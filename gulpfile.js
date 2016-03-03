var gulp = require('gulp');
var ngAnnotate = require('gulp-ng-annotate');
var uglify = require('gulp-uglify');
var watch = require('gulp-watch');
var shell = require('gulp-shell');
var notify = require('gulp-notify');
var plumber = require('gulp-plumber');
var gutil = require('gulp-util');

gulp.task('default', ['build'], function () {
});

gulp.task('build', function () {
  return gulp.src('static/javascripts/**/*.js')
    //.pipe(ngAnnotate())
    //.pipe(uglify())
    .pipe(plumber({
        errorHandler: reportError
    }))
    .pipe(uglify())
    .on('error', reportError)
    .pipe(gulp.dest('static/dist/javascripts/'));
});

// default gulp task
gulp.task('default', ['build'], function() {
  // watch for JS changes
  gulp.watch('static/javascripts/**/*.js', function() {
    gulp.run('build');
  });
});

var reportError = function (error) {
    var lineNumber = (error.lineNumber) ? 'LINE ' + error.lineNumber + ' -- ' : '';

    notify({
        title: 'Task Failed [' + error.plugin + ']',
        message: lineNumber + 'See console.',
        sound: 'Sosumi' // See: https://github.com/mikaelbr/node-notifier#all-notification-options-with-their-defaults
    }).write(error);

    gutil.beep(); // Beep 'sosumi' again

    // Inspect the error object
    // console.log(error);

    // Easy error reporting
    // console.log(error.toString());

    // Pretty error reporting
    var report = '';
    var chalk = gutil.colors.white.bgRed;

    report += chalk('TASK:') + ' [' + error.plugin + ']\n';
    report += chalk('PROB:') + ' ' + error.message + '\n';
    if (error.lineNumber) { report += chalk('LINE:') + ' ' + error.lineNumber + '\n'; }
    if (error.fileName)   { report += chalk('FILE:') + ' ' + error.fileName + '\n'; }
    console.error(report);

    // Prevent the 'watch' task from stopping
    this.emit('end');
}