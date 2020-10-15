import { Component, OnInit, ViewChild } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort, MatSortable } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { Subscription } from 'rxjs';
import { map } from 'rxjs/internal/operators/map';
import { Player } from '../player';
import { PlayersService } from '../players.service';

@Component({
  selector: 'app-players',
  templateUrl: './players.component.html',
  styleUrls: ['./players.component.css']
})
export class PlayersComponent implements OnInit {
  private subscription: Subscription;
  displayedColumns = ['id', 'name', 'country'];
  dataSource: MatTableDataSource<Player>;

  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;

  constructor(private playersService: PlayersService) { }

  ngOnInit() {
    console.log('initializing players');
    this.dataSource = new MatTableDataSource();
    this.getPlayers();
  }

  ngAfterViewInit() {
    this.paginator.pageSize = 10;
    this.dataSource.paginator = this.paginator;
    this.sort.sort(({ id: 'name', start: 'asc' }) as MatSortable);
    this.dataSource.sort = this.sort;
  }

  ngOnDestroy() {
    this.subscription.unsubscribe();
  }

  applyFilter(filterValue: string) {
    filterValue = filterValue.trim();
    filterValue = filterValue.toLowerCase();
    this.dataSource.filter = filterValue;
  }

  getPlayers(): void {
    this.subscription = this.playersService.getPlayers().subscribe(
      players => this.dataSource.data = players
    )
  }

}
