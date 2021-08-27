import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { GraphComponent } from './graph/graph.component';
import { ChatboxComponent } from './chatbox/chatbox.component';

@NgModule({
  declarations: [AppComponent, GraphComponent, ChatboxComponent],
  imports: [BrowserModule, HttpClientModule],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
