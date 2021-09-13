import { Injectable } from '@angular/core';
import { timer, of, BehaviorSubject } from 'rxjs';
import { exhaustMap } from 'rxjs/operators';

export const initialData = {
  nodes: [
    { type: 'User', id: 0, name: 'Alice', group: 0 },
    { type: 'User', id: 1, name: 'Bob', group: 0 },
    { type: 'User', id: 2, name: 'Charlie', group: 0 },
    { type: 'Submission', id: 8, name: 'submission A', group: 1 },
    { type: 'Submission', id: 9, name: 'submission B', group: 1 },
    { type: 'Comment', id: 10, text: 'A', group: 2 },
    { type: 'Comment', id: 11, text: 'B', group: 2 },
    { type: 'Comment', id: 12, text: 'C', group: 2 },
    { type: 'Comment', id: 13, text: 'D', group: 2 },
    { type: 'Comment', id: 14, text: 'E', group: 2 },
    { type: 'Comment', id: 15, text: 'F', group: 2 },
    { type: 'Comment', id: 16, text: 'G', group: 2 },
    { type: 'Comment', id: 17, text: 'H', group: 2 },
    { type: 'Comment', id: 18, text: 'I', group: 2 },
  ],
  links: [
    { source: 10, target: 8 },
    { source: 11, target: 8 },
    { source: 12, target: 8 },
    { source: 13, target: 8 },
    { source: 14, target: 8 },
    { source: 15, target: 9 },
    { source: 16, target: 11 },
    { source: 17, target: 11 },
    { source: 18, target: 13 },

    { source: 10, target: 0 },
    { source: 11, target: 0 },
    { source: 12, target: 0 },
    { source: 13, target: 1 },
    { source: 14, target: 1 },
    { source: 15, target: 2 },
    { source: 16, target: 2 },
    { source: 17, target: 1 },
    { source: 18, target: 0 },
  ],
};

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  commentId = 19;

  public data$ = new BehaviorSubject<any>(initialData);

  public getData() {
    const data = this.data$.getValue();

    data.nodes.push({
      id: this.commentId,
      type: 'Comment',
      group: 2,
      text: 'new',
    });
    const randomUserId = Math.round(Math.random() * 1000) % 3;
    const randomCommentId = (Math.round(Math.random() * 1000) % (this.commentId - 8)) + 8;
    data.links.push(
      {
        source: this.commentId,
        target: randomUserId,
      },
      {
        source: this.commentId,
        target: randomCommentId,
      },
    );
    this.commentId += 1;

    return of(data);
  }

  public startListening() {
    timer(1000, 5000)
      .pipe(exhaustMap(() => this.getData()))
      .subscribe((data) => {
        this.data$.next(data);
      });
  }
}
