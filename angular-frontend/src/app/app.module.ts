import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { PlayerComponent } from './player/player.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { DetailComponent } from './detail/detail.component';
import { BracketComponent } from './bracket/bracket.component';
import { TournamentsComponent } from './tournaments/tournaments.component';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatSortModule } from '@angular/material/sort';
import { MatTableModule } from '@angular/material/table';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { PlayersComponent } from './players/players.component';
import { TournamentComponent } from './tournament/tournament.component';
import { IconsModule } from './icons/icons.module';
import { MainPipe } from './main-pipe.module';

@NgModule({
  declarations: [
    AppComponent,
    PlayerComponent,
    DashboardComponent,
    DetailComponent,
    BracketComponent,
    TournamentsComponent,
    PlayersComponent,
    TournamentComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    MatPaginatorModule,
    MatSortModule,
    MatTableModule,
    MatInputModule,
    MatFormFieldModule,
    BrowserAnimationsModule,
    IconsModule,
    MainPipe
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
