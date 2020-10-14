import { TestBed } from '@angular/core/testing';

import { MatchupsService } from './matchups.service';

describe('MatchupsService', () => {
  let service: MatchupsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(MatchupsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
