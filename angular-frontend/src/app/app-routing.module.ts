import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component';
import { PlayersComponent } from './players/players.component';
import { PlayerComponent } from './player/player.component';
import { BracketComponent } from './bracket/bracket.component';
import { TournamentsComponent } from './tournaments/tournaments.component';
import { TournamentComponent } from './tournament/tournament.component';

const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'players', component: PlayersComponent },
  { path: 'player/:id', component: PlayerComponent },
  { path: 'tournaments', component: TournamentsComponent },
  { path: 'tournament/:id', component: TournamentComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
