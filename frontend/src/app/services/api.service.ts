import '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import * as socketIo from 'socket.io-client';

const Groups: { [key: string]: number } = {
  REDDITOR: 0,
  SUBMISSION: 1,
  COMMENT: 2,
};

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

  public initSocket(): void {
    this.socket = socketIo('ws://localhost:5000');
    this.socket.emit('consumer');
  }

  public sendMe(message: any): void {
    this.socket.emit('message', { data: message });
  }

  // previously onMessage
  public startPolling() {
    this.socket.on('consumer', (data: any) => {
      console.log('Received a message from websocket service');
      const currentData = this.data$.getValue();
      const nodes = data.data.vertices.map((vertex) => {
        return {
          id: vertex.id,
          type: vertex.labels[0],
          group: Groups[vertex.labels[0]],
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
