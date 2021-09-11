import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { GraphComponent } from './graph/graph.component';
import { LiveFeedComponent } from './live-feed/live-feed.component';

@NgModule({
  declarations: [AppComponent, GraphComponent, LiveFeedComponent],
  imports: [BrowserModule, HttpClientModule],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
