import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './components/app/app.component';
import { GraphComponent } from './components/graph/graph.component';
import { LiveFeedComponent } from './components/live-feed/live-feed.component';

@NgModule({
  declarations: [AppComponent, GraphComponent, LiveFeedComponent],
  imports: [BrowserModule, HttpClientModule],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
