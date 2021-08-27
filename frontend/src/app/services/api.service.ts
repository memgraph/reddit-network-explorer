import '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import * as socketIo from 'socket.io-client';

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
          ...this.getStyle(vertex.labels[0], vertex.sentiment),
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
      console.log('data', currentData);
      this.data$.next(currentData);
    });
  }

  public onEvent(event: Event): Observable<any> {
    return new Observable<Event>((observer) => {
      this.socket.on(event, () => observer.next());
    });
  }

  private getStyle(type, sentiment) {
    if (type === 'COMMENT') {
      const radius = 7;
      let color = '#989898';
      if (sentiment === -1) {
        color = '#ff0000';
      }
      if (sentiment === 1) {
        color = '#00ff00';
      }
      return { color, radius };
    }
    if (type === 'REDDITOR') {
      return { color: '#0000ff', radius: 5 };
    }
    if (type === 'SUBMISSION') {
      const radius = 10;
      let color = '#585858';
      if (sentiment === -1) {
        color = '#F2543D';
      }
      if (sentiment === 1) {
        color = '#38C477';
      }
      return { color, radius };
    }
    return { color: '#ef42f5', radius: 3 };
  }
}
