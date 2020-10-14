import { Component, OnInit } from '@angular/core';
import { Player } from '../player';
import { PlayersService } from '../players.service';

@Component({
  selector: 'app-detail',
  templateUrl: './detail.component.html',
  styleUrls: ['./detail.component.css'],
})
export class DetailComponent implements OnInit {
  player: Player;

  constructor(private playersService: PlayersService) {}

  ngOnInit() {
    this.getPlayers();
  }

  getPlayers(): void {
    this.playersService.getPlayers().subscribe(
      players => this.player = players[0]
    )
  }
}
