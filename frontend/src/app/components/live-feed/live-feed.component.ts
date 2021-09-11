import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { map } from 'rxjs/operators';

@Component({
  selector: 'app-live-feed',
  templateUrl: './live-feed.component.html',
  styleUrls: ['./live-feed.component.scss'],
})
export class LiveFeedComponent implements OnInit {
  comments$;

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.comments$ = this.api.data$.pipe(
      map((data: any) => data.nodes.filter((node) => node.type === 'COMMENT' || node.type === 'SUBMISSION').reverse()),
    );
  }
}
