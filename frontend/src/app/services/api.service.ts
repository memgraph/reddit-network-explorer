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

  public getGraph() {
    this.httpClient.get('/api/graph').subscribe((res) => {
      console.log(res);
    });
  }

  public startPolling() {
    this.socket.on('consumer', (data: any) => {
      console.log('Received a message from websocket service');
      const currentData = this.data$.getValue();
      console.log('data', data.data);
      const nodes = data.data.vertices.map((vertex) => {
        return {
          id: vertex.id,
          type: vertex.labels[0],
          text: vertex.name || vertex.body || vertex.title,
          ...getStyle(vertex.labels[0], vertex.sentiment),
        };
      });
      const links = data.data.edges.map((edge) => {
        return {
          id: edge.id,
          source: edge.from,
          target: edge.to,
          type: edge.type,
        };
      });
      this.datum$.next({ nodes, links });
      currentData.nodes = currentData.nodes.concat(nodes);
      currentData.links = currentData.links.concat(links);
      this.data$.next(currentData);
    });
  }

  public onEvent(event: Event): Observable<any> {
    return new Observable<Event>((observer) => {
      this.socket.on(event, () => observer.next());
    });
  }
}
