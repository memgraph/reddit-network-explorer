import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { delay, shareReplay } from 'rxjs/operators';
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

  private _data$ = new BehaviorSubject<any>(initialData);
  private _datum$ = new BehaviorSubject<any>(initialData);

  data$ = this._data$.asObservable().pipe(shareReplay());
  datum$ = this._datum$.asObservable().pipe(shareReplay());

  constructor(private httpClient: HttpClient) {}

  public initSocket(): void {
    this.socket = socketIo('ws://localhost:5000');
    this.socket.emit('consumer');
  }

  /**
   * Fetches the initial graph
   */
  public getGraph() {
    this.httpClient
      .get('/api/graph')
      .pipe(delay(2000))
      .subscribe((res: any) => {
        this.updateData(res);
      });
  }

  /**
   * Start listening for new streaming data (nodes and links) on the WebSocket.
   */
  public startListening() {
    this.socket.on('consumer', (res: any) => {
      console.log('Received a message from the WebSocket service: ', res);
      this.updateData(res.data);
    });
  }

  public onEvent(event: Event): Observable<any> {
    return new Observable<Event>((observer) => {
      this.socket.on(event, () => observer.next());
    });
  }

  /**
   * Adds additional properties such as styles, D3 compatible names, etc.
   */
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

  /*
    Transforms and emits new data coming from the stream.
  */
  private updateData(data) {
    // Add additional properties such as styles, D3 compatible names, etc.
    const transformedData = this.transformData(data);

    // Get current data
    const currentData = this._data$.getValue();

    // Update current nodes
    const nodes = transformedData.nodes;
    currentData.nodes = currentData.nodes.concat(nodes);

    // Filter out invalid links - links without both source and target nodes
    const links = transformedData.links.filter((link) => {
      return (
        currentData.nodes.find((node) => node.id === link.source) &&
        currentData.nodes.find((node) => node.id === link.target)
      );
    });
    currentData.links = currentData.links.concat(links);

    // Emit new incoming data
    this._datum$.next({ nodes, links });

    // Update and emit all existing data
    this._data$.next(currentData);
  }
}
