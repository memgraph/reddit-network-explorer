import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import * as socketIo from 'socket.io-client';

import { getStyle } from '../utils/style.util';

export const initialData = { nodes: [], links: [] };

export enum Event {
  CONNECT = 'connect',
  DISCONNECT = 'disconnect',
}

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private socket;

  data$ = new BehaviorSubject<any>(initialData);
  datum$ = new BehaviorSubject<any>(initialData);

  constructor(private httpClient: HttpClient) {}

  public initSocket(): void {
    this.socket = socketIo('ws://localhost:5000');
    this.socket.emit('consumer');
  }

  // Gets the initial graph
  public getGraph() {
    this.httpClient.get('/api/graph').subscribe((res: any) => {
      this.updateData(res);
    });
  }

  // Start listening for new streaming data (nodes and links) on the WebSocket.
  public startListening() {
    this.socket.on('consumer', (res: any) => {
      console.log('Received a message from websocket service');
      this.updateData(res.data);
    });
  }

  public onEvent(event: Event): Observable<any> {
    return new Observable<Event>((observer) => {
      this.socket.on(event, () => observer.next());
    });
  }

  // Adds additional properties such as styles, D3 compatible names, etc.
  private transformData(data: any) {
    const nodes = data.vertices.map((vertex) => {
      return {
        id: vertex.id,
        type: vertex.labels[0],
        text: vertex.name || vertex.body || vertex.title,
        ...getStyle(vertex.labels[0], vertex.sentiment),
      };
    });
    const links = data.edges.map((edge) => {
      return {
        id: edge.id,
        source: edge.from,
        target: edge.to,
        type: edge.type,
      };
    });

    return { nodes, links };
  }

  // Transforms and emits new data coming from the stream.
  private updateData(data) {
    // Add additional properties such as styles, D3 compatible names, etc.
    const transformedData = this.transformData(data);

    // Emit new incoming data
    const nodes = transformedData.nodes;
    const links = transformedData.links;
    this.datum$.next({ nodes, links });

    // Update and emit all existing data
    const currentData = this.data$.getValue();
    currentData.nodes = currentData.nodes.concat(nodes);
    currentData.links = currentData.links.concat(links);
    this.data$.next(currentData);
  }
}
