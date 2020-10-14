import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';

import { Player } from './player';

@Injectable({
  providedIn: 'root'
})
export class PlayersService {
  private playersUrl = 'https://atptennisapi.freeddns.org/players';
  private playerUrl = 'https://atptennisapi.freeddns.org/player';

  constructor(private http: HttpClient) { }

  public getPlayers(): Observable<Player[]> {

    return this.http.get<Player[]>(this.playersUrl).pipe(
      tap((result) => result),
      catchError(result => of(result as Player[]))
    );
  }

  public getPlayer(id: number): Observable<Player> {

    return this.http.get<Player>(`${this.playerUrl}?id=${id}`).pipe(
      tap((result) => result),
      catchError(result => of(result as Player))
    );
  }
}
