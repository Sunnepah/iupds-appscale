var gulp = require('gulp');
var ngAnnotate = require('gulp-ng-annotate');
var uglify = require('gulp-uglify');
var watch = require('gulp-watch');
var shell = require('gulp-shell')

gulp.task('default', ['build'], function () {
});

gulp.task('build', function () {
  return gulp.src('static/javascripts/**/*.js')
    .pipe(ngAnnotate())
    .pipe(uglify())
    .pipe(gulp.dest('static/dist/javascripts/'));
//    .pipe(shell([
//      'python manage.py collectstatic'
//    ]))
});

// default gulp task
gulp.task('default', ['build'], function() {
  // watch for JS changes
  gulp.watch('static/javascripts/**/*.js', function() {
    gulp.run('build');
  });
});
