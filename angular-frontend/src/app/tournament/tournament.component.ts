import { Component, OnInit } from '@angular/core';
import { Tournament } from '../tournament';
import { TournamentsService } from '../tournaments.service';
import { Location } from '@angular/common';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-tournament',
  templateUrl: './tournament.component.html',
  styleUrls: ['./tournament.component.css'],
})
export class TournamentComponent implements OnInit {
  tournament: Tournament;

  constructor(
    private route: ActivatedRoute,
    private tournamentsService: TournamentsService,
    private location: Location
  ) {}

  ngOnInit() {
    this.getTournament();
  }

  getTournament(): void {
    const id = +this.route.snapshot.paramMap.get('id');
    this.tournamentsService
      .getTournament(id)
      .subscribe((tournament) => (this.tournament = tournament));
  }

  getShortDate(longDate: string) {
    var d = new Date(Date.parse(longDate));
    return `${d.getFullYear()}` + 
      `-${d.getMonth() < 9 ? '0' + (d.getMonth() + 1) : (d.getMonth() + 1)}` +
      `-${d.getDate() < 10 ? '0' + (d.getDate()) : (d.getDate())}`
  }

  goBack(): void {
    this.location.back();
  }
}
