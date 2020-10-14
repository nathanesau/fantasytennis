import { HttpClient, HttpUrlEncodingCodec } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { Matchup } from './matchup';

@Injectable({
  providedIn: 'root',
})
export class MatchupsService {
  //private matchupsUrl =
  //  'https://atptennisapi.freeddns.org/matchups?tournament_name=Beijing&tournament_start_date=Mon%2C%2003%20Oct%202016%2000%3A00%3A00%20GMT';
  private matchupsUrl = 'https://atptennisapi.freeddns.org/matchups';

  constructor(private http: HttpClient) {}

  public getMatchups(
    tournamentName: string,
    tournamentStartDate: string
  ): Observable<Matchup[]> {
    return this.http
      .get<Matchup[]>(this.getMatchupsUrl(tournamentName, tournamentStartDate))
      .pipe(
        tap((result) => result),
        catchError((result) => of(result as Matchup[]))
      );
  }

  private getMatchupsUrl(
    tournamentName: string,
    tournamentStartDate: string
  ): string {
    var name = tournamentName;
    var start = tournamentStartDate;
    return encodeURI(
      `${this.matchupsUrl}?tournament_name=${name}&tournament_start_date=${start}`
    );
  }
}
