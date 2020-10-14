import { Component, OnInit, ViewChild } from '@angular/core';
import { Tournament } from '../tournament';
import { TournamentsService } from '../tournaments.service';
import { MatPaginator, MatPaginatorModule } from '@angular/material/paginator';
import { MatTable, MatTableDataSource } from '@angular/material/table';
import { MatSort, MatSortable } from '@angular/material/sort';
import { map, retry } from 'rxjs/operators';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-tournaments',
  templateUrl: './tournaments.component.html',
  styleUrls: ['./tournaments.component.css']
})
export class TournamentsComponent implements OnInit {
  private subscription: Subscription;
  displayedColumns = ['id', 'name', 'start', 'end'];
  dataSource: MatTableDataSource<Tournament>;

  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort) sort: MatSort;

  constructor(private tournamentsService: TournamentsService) { }

  sleep(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async poll() {
    var att = 1;
    while (this.dataSource.data.length == 0 && att < 5) {
      await this.sleep(5000);
      this.getTournaments();
      att += 1;
    }
  }

  ngOnInit() {
    console.log('initializing tournaments');
    this.dataSource = new MatTableDataSource();
    this.getTournaments();
    this.poll();
  }

  ngAfterViewInit() {
    this.paginator.pageSize = 10;
    this.dataSource.paginator = this.paginator;
    this.sort.sort(({ id: 'start', start: 'desc' }) as MatSortable);
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

  getTournaments(): void {
    this.subscription = this.tournamentsService.getTournaments()
      .subscribe(
        tournaments => {
          this.dataSource.data = tournaments.map(tournament => {
            tournament.start = this.getShortDate(tournament.start);
            tournament.end = this.getShortDate(tournament.end);
            return tournament;
          })
        })
  }

  getShortDate(longDate: string) {
    var d = new Date(Date.parse(longDate));
    return `${d.getFullYear()}` +
      `-${d.getMonth() < 9 ? '0' + (d.getMonth() + 1) : (d.getMonth() + 1)}` +
      `-${d.getDate() < 10 ? '0' + (d.getDate()) : (d.getDate())}`
  }

}
