import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ChatboxComponent } from './chatbox.component';

describe('ChatboxComponent', () => {
  let component: ChatboxComponent;
  let fixture: ComponentFixture<ChatboxComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ChatboxComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ChatboxComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
