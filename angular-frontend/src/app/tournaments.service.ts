import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';
import { Tournament } from './tournament';

@Injectable({
  providedIn: 'root'
})
export class TournamentsService {
  private tournamentsUrl = 'https://atptennisapi.freeddns.org/tournaments';
  private tournamentUrl = 'https://atptennisapi.freeddns.org/tournament';

  constructor(private http: HttpClient) { }

  public getTournaments(): Observable<Tournament[]> {

    return this.http.get<Tournament[]>(this.tournamentsUrl).pipe(
      tap((result) => result),
      catchError(result => {
        return of(result as Tournament[])
      })
    );
  }

  public getTournament(id: number): Observable<Tournament> {

    return this.http.get<Tournament>(`${this.tournamentUrl}?id=${id}`).pipe(
      tap((result) => result),
      catchError(result => of(result as Tournament))
    );
  }
}
