import { Component, OnInit } from '@angular/core';
import { Player } from '../player';
import { PlayersService } from '../players.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css'],
})
export class DashboardComponent implements OnInit {

  players: Player[];

  constructor() {}

  ngOnInit() {
  }

}
