import { NgModule } from '@angular/core';

import { FeatherModule } from 'angular-feather';
import { Camera, Heart, Github } from 'angular-feather/icons';

const icons = {
  Camera,
  Heart,
  Github
};

@NgModule({
  imports: [
    FeatherModule.pick(icons)
  ],
  exports: [
    FeatherModule
  ]
})
export class IconsModule { }