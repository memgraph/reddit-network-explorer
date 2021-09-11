import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LiveFeedComponent } from './live-feed.component';

describe('LiveFeedComponent', () => {
  let component: LiveFeedComponent;
  let fixture: ComponentFixture<LiveFeedComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [LiveFeedComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(LiveFeedComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
