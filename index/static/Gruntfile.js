module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
	
	less: {
      develop: {
        options: {
          strictMath: true,
          sourceMap: true,
          outputSourceFiles: true,
          sourceMapURL: '<%= pkg.name %>.css.map',
          sourceMapFilename: 'dist/css/<%= pkg.name %>.css.map'
        },
        files: {
        	'dist/css/<%= pkg.name %>.css': ['less/bootstrap-tenant.less'],
        }
      },
      minify: {
    		options: {
    			cleancss: true,
    			report: 'min'
    		},
    		files: {
    			'dist/css/<%= pkg.name %>.min.css': 'dist/css/<%= pkg.name %>.css'
    		}
      }
    },

    watch: {
  		less: {
  			files: 'less/*.less',
  			tasks: 'less'
  		}
    },

    uglify: {
      options: {
        report: 'min'
      },
      bootstrap: {
        options: {
          banner: '<%= banner %>'
        },
        src: '<%= concat.bootstrap.dest %>',
        dest: 'dist/js/<%= pkg.name %>.min.js'
      }
    },

    concat: {
      options: {
        banner: '<%= banner %>\n<%= jqueryCheck %>',
        stripBanners: false
      },
      bootstrap: {
        src: [
          'bower_components/bootstrap/js/transition.js',
          // 'bower_components/bootstrap/js/alert.js',
          // 'bower_components/bootstrap/js/button.js',
          // 'bower_components/bootstrap/js/carousel.js',
          'bower_components/bootstrap/js/collapse.js',
          // 'bower_components/bootstrap/js/dropdown.js',
          // 'bower_components/bootstrap/js/modal.js',
          // 'bower_components/bootstrap/js/tooltip.js',
          // 'bower_components/bootstrap/js/popover.js',
          // 'bower_components/bootstrap/js/scrollspy.js',
          // 'bower_components/bootstrap/js/tab.js',
          // 'bower_components/bootstrap/js/affix.js'
        ],
        dest: 'dist/js/<%= pkg.name %>.js'
      }
    },

    copy: {
      fonts: {
        expand: true,
        flatten: true,
        src: './bower_components/bootstrap/fonts/*',
        dest: './dist/fonts/'
      }
    },

    clean: {
      dist: ['dist']
    }

  });

	// These plugins provide necessary tasks.
	require('load-grunt-tasks')(grunt, {scope: 'devDependencies'});

	// Default task(s).
	grunt.registerTask('default', ['watch']);

	// JS distribution task.
	grunt.registerTask('dist-js', ['concat', 'uglify']);

	// Full dist.
	grunt.registerTask('dist', ['clean', 'less', 'dist-js', 'copy:fonts']);

};