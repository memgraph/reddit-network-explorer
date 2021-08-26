import '@angular/common/http';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import * as socketIo from 'socket.io-client';

export enum Event {
  CONNECT = 'connect',
  DISCONNECT = 'disconnect',
}

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  socket;
  data$ = new BehaviorSubject<any>({ nodes: [], links: [] });
  index = 0;

  constructor(private http: HttpClient) {
    /*
    this.socket = webSocket('wss://localhost:5000');
    this.socket.subscribe(
      (msg) => console.log('msg', msg),
      (err) => console.log('err', err),
      () => console.log('complete'),
    );
    */
  }

  public initSocket(): void {
    this.socket = socketIo('ws://localhost:5000');
    this.socket.emit('consumer');
  }

  // This method is used to send message to backend
  public sendMe(message: any): void {
    this.socket.emit('message', { data: message });
  }

  public onMessage(): Observable<any> {
    return new Observable<any>((observer) => {
      // This below method is not firing
      this.socket.on('consumer', (data: any) => {
        console.log('Received a message from websocket service');
        console.log('data', data);
        console.log('json', JSON.parse(data.data));
        observer.next(JSON.parse(data));
      });
    });
  }

  // This gets called on connect and disconnect event.
  public onEvent(event: Event): Observable<any> {
    return new Observable<Event>((observer) => {
      this.socket.on(event, () => observer.next());
    });
  }
}
