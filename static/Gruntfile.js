<!-- code begin -->
module.exports = function(grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),  
    less: {
      development: {
        options: {
          compress: false,
          yuicompress: false
        },
        files: {
          "css/user/bind.css": "less/user/bind.less",
          "css/base.css": "less/base.less"
        }
      },
      production: {
        options: {
          modifyVars: {
            imagepath_page: '"/img/"',
            imagepath: '"/img/"'
          },
          compress: true,
          yuicompress: true,
          optimization: 2,
        },
        files: {
          "css/user/bind.css": "less/user/bind.less",
          "css/base.css": "less/base.less"
        }
      }
    },     
    watch: {
      grunt: {
        files: ['Gruntfile.js']
      },
      development: {
        files: [
          'less/**/*.less',
          'less/*.less',
          'css/**/*.css',
          'css/*.css',
          'u/*.html',
          'u/**/*.html',
          'student/*.html',
          'student/**/*.html',
          'teacher/*.html',
          'teacher/**/*.html'
        ],
        tasks:['less:development'],
        options: {
          nospawn: true,
          livereload: true,
        }
      },
      production: {
        files: [
          'less/**/*.less',
          'less/*.less',
          'css/**/*.css',
          'css/*.css',
          'u/*.html',
          'u/**/*.html',
          'student/*.html',
          'student/**/*.html',
          'teacher/*.html',
          'teacher/**/*.html'
        ],
        tasks:['less:production'],
        options: {
          nospawn: true,
          livereload: true,
        }
      },
    }    
  });
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.registerTask('default', ['watch:development']);
  grunt.registerTask('production', ['less:production'])
};
<!-- code end -->