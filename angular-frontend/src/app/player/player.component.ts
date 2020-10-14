import { Component, OnInit } from '@angular/core';
import { Player } from '../player';
import { PlayersService } from '../players.service';
import { Location } from '@angular/common';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-player',
  templateUrl: './player.component.html',
  styleUrls: ['./player.component.css'],
})
export class PlayerComponent implements OnInit {
  player: Player;

  constructor(
    private route: ActivatedRoute,
    private playersService: PlayersService,
    private location: Location
  ) {}

  ngOnInit() {
    this.getPlayer();
  }

  getPlayer(): void {
    const id = +this.route.snapshot.paramMap.get('id');
    this.playersService
      .getPlayer(id)
      .subscribe((player) => (this.player = player));
  }

  goBack(): void {
    this.location.back();
  }
}
