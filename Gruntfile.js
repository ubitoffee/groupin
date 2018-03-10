/**
 * Created by JSY on 2017-07-08.
 */


module.exports = function (grunt) {

  'use strict';

  grunt.initConfig({
    watch: {
      files: ["web/static/less/*.less", "web/build/less/skins/*.less", "web/static/js/app.js"],
      tasks: ["less", "uglify"]
    },
    /* LESS Compile */
    less: {
      development: {
        options: {
          compress: false
        },
        files: {
          "web/dist/css/base.css": "web/static/less/base.less",
        }
      },
      production: {
        options: {
          compress: true
        },
        files: {
          "web/dist/css/base.css": "web/static/less/base.less",
        }
      }
    },
    /* Javascript Uglify */
    uglify: {
      options: {
        mangle: true,
        preserveComments: 'some'
      },
      my_target: {
        files: {
          'web/dist/js/app.js': ['web/static/js/app.js']
        }
      }
    },
    /* Image Compression */
    image: {
      dynamic: {
        files: [{
          expand: true,
          cwd: 'web/static/img/',
          src: ['**/*.{png,jpg,gif,svg,jpeg}'],
          dest: 'web/dist/img/'
        }]
      }
    },

    // Validate JS code
    jshint: {
      options: {
        jshintrc: '.jshintrc'
      },
      core: {
        src: 'web/static/js/app.js'
      }
    },

    csslint: {
      options: {
        csslintrc: 'web/static/less/.csslintrc'
      },
      dist: [
        'web/dist/css/base.css',
      ]
    },

    /* Compression 전 이미지 삭제 */
    clean: {
      build: ["web/static/img/*"]
    }
  });

  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-image');
  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-clean');
  grunt.loadNpmTasks('grunt-contrib-csslint');

  grunt.registerTask('default', ['watch']);
};