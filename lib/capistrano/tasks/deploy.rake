after 'deploy:updating', 'python:create_virtualenv'
after 'deploy:cleanup', 'deploy:restart'
# after 'deploy:updating', 'python:install_python'

namespace :deploy do
  desc 'Restart application'
  task :restart do
      if fetch(:nginx)
          invoke 'deploy:nginx_restart'
      else
          on roles(:web) do |h|
              execute "sudo apache2ctl graceful"
          end
      end
  end

  task :nginx_restart do
    on roles(:web) do
      within release_path do
        if fetch(:app_server) == 'uwsgi'

          uwsgi = "#{shared_path}/virtualenv/bin/uwsgi"
          pid_file = "#{shared_path}/uwsgi.pid"
          shared_dir_list = capture("ls #{shared_path}").split()
          if shared_dir_list.include? 'uwsgi.pid'
            execute uwsgi, '--stop', pid_file
          end
          execute "for KILLPID in `ps wx | grep 'uwsgi' | grep '#{fetch(:application)}' | awk ' { print $1;}'`; do kill -9 $KILLPID; done"
          execute uwsgi, '--ini', "#{release_path}/uwsgi.ini"
        end
        if fetch(:app_server) == 'gunicorn'
          pid_file = "#{releases_path}/gunicorn.pid"
          if test "[ -e #{pid_file} ]"
            execute "kill `cat #{pid_file}`"
          end
          execute "virtualenv/bin/gunicorn", "#{fetch(:wsgi_file)}:application", '-c=gunicorn_config.py', "--pid=#{pid_file}"
        end
      end
    end
  end
end

namespace :django do

  def django(args, flags="", run_on=:all)
    on roles(run_on) do |h|
      manage_path = File.join(release_path, fetch(:django_project_dir) || '', 'manage.py')
      execute "#{release_path}/virtualenv/bin/python #{manage_path} #{args} #{flags}"
    end
  end

  # after 'deploy:restart', 'django:restart_celery'

  desc "Symlink shared settings"
  task :link_settings do
    if fetch(:shared_django_settings)
      on roles(:all) do
        unless test("[ -e #{File.join(release_path, '#{fetch(:application)}/settings.py')} ]")
          # execute :ln, '-s', File.join(shared_path, fetch(:django_settings)), File.join(release_path, 'ad_folders/settings.py')
          execute :cp, File.join(shared_path, fetch(:django_settings)), File.join(release_path, "#{fetch(:application)}/settings.py")
        end
      end
    end
  end

  desc "Symlink UWSGi settings"
  task :link_uwsgi do
    on roles(:app) do
      execute :cp, File.join(shared_path, fetch(:uwsgi_settings)), File.join(release_path, "uwsgi.ini")
    end
  end

  desc "Symlink migrations"
  task :link_migrations do
    on roles(:all) do
      fetch(:project_apps).each { |app|
        app_migrations_path = File.join(shared_path, 'migrations', app, 'migrations')
        # unless File.exist?(app_migrations_path)
        #   execute :mkdir, app_migrations_path
        # end
        execute :ln, '-s', app_migrations_path, File.join(release_path, app, 'migrations')
      }
    end
  end

  desc "Symlink media folder"
  task :link_media do
    on roles(:all) do
      execute :ln, '-s', File.join(shared_path, 'media'), File.join(release_path, 'media')
    end
  end

  desc "Setup Django environment"
  task :setup do
    if fetch(:shared_django_settings)
      puts 'Shared'
      invoke 'django:link_settings'
    end
    
    invoke 'django:link_migrations'
    
    if fetch(:django_compressor)
      invoke 'django:compress'
    end
    invoke 'django:link_media'
    invoke 'django:compilemessages'
    invoke 'django:collectstatic'
    # invoke 'django:symlink_settings'
    if !fetch(:nginx)
      invoke 'django:symlink_wsgi'
    end
    invoke 'django:makemigrations'
    invoke 'django:migrate'
    invoke 'django:link_uwsgi'
    if fetch(:use_celery)
        puts fetch(:use_celery)
        invoke 'django:start_celery'
    end
  end

  desc "Compile Messages"
  task :compilemessages do
    if fetch :compilemessages
      django("compilemessages")
    end
  end

  desc "Stop Celery"
  task :stop_celery do
    on roles(:app) do
      if fetch(:use_pyenv)
        venv_name = "#{fetch(:application)}-#{fetch(:python_version)}"
        virtualenv_path = "~/.pyenv/versions/#{venv_name}"
      else
        virtualenv_path = File.join(
            fetch(:shared_virtualenv) ? shared_path : release_path, "virtualenv"
        )
      end
      celery_path = File.join(virtualenv_path, 'bin', 'celery')
      execute "cd #{release_path}; #{celery_path} multi stop #{fetch(:celery_name)} --pidfile=#{File.join(shared_path, 'celeryd.pid')}"
    end
  end

  desc "Start Celery"
  task :start_celery do
    on roles(:app) do
      if fetch(:use_pyenv)
        venv_name = "#{fetch(:application)}-#{fetch(:python_version)}"
        virtualenv_path = "~/.pyenv/versions/#{venv_name}"
      else
        virtualenv_path = File.join(
            fetch(:shared_virtualenv) ? shared_path : release_path, "virtualenv"
        )
      end
      celery_path = File.join(virtualenv_path, 'bin', 'celery')
      execute "cd #{release_path}; #{celery_path} multi start #{fetch(:celery_name)} -A #{fetch(:application)} --beat -c4 --pidfile=#{File.join(release_path, 'celeryd.pid')} --logfile=#{File.join(shared_path, 'celeryd.log')}"
      execute "rm -f #{shared_path}/celeryd.pid"
      execute "ln -s #{File.join(release_path, 'celeryd.pid')} #{File.join(shared_path, 'celeryd.pid')}"
    end
  end


  # desc "Restart Celery"
  # task :restart_celery do
  #   if fetch(:celery_name)
  #     invoke 'django:restart_celeryd'
  #     invoke 'django:restart_celerybeat'
  #   end
  #   if fetch(:celery_names)
  #     invoke 'django:restart_named_celery_processes'
  #   end
  # end

  # desc "Restart Celeryd"
  # task :restart_celeryd do
  #   on roles(:jobs) do
  #     execute "sudo service celeryd-#{fetch(:celery_name)} restart"
  #   end
  # end

  # desc "Restart Celerybeat"
  # task :restart_celerybeat do
  #   on roles(:jobs) do
  #     execute "sudo service celerybeat-#{fetch(:celery_name)} restart"
  #   end
  # end

  # desc "Restart named celery processes"
  # task :restart_named_celery_processes do
  #   on roles(:jobs) do
  #     fetch(:celery_names).each { | celery_name, celery_beat |
  #       execute "sudo service celeryd-#{celery_name} restart"
  #       if celery_beat
  #         execute "sudo service celerybeat-#{celery_name} restart"
  #       end
  #     }
  #   end
  # end

  desc "Run django-compressor"
  task :compress do
    django("compress")
  end

  desc "Run django's collectstatic"
  task :collectstatic do
    if fetch(:create_s3_bucket)
      invoke 's3:create_bucket'
      on roles(:web) do
        django("collectstatic", "-i *.coffee -i *.less -i node_modules/* -i bower_components/* --noinput --clear")
      end
    else
      django("collectstatic", "-i *.coffee -i *.less -i node_modules/* -i bower_components/* --noinput")
    end
  end

  # desc "Symlink django settings to deployed.py"
  # task :symlink_settings do
  #   settings_path = File.join(release_path, fetch(:django_settings_dir))
  #   on roles(:all) do
  #     execute "ln -s #{settings_path}/#{fetch(:django_settings)}.py #{settings_path}/deployed.py"
  #   end
  # end

  desc "Symlink wsgi script to live.wsgi"
  task :symlink_wsgi do
    on roles(:web) do
      wsgi_path = File.join(release_path, fetch(:wsgi_path, 'wsgi'))
      wsgi_file_name = fetch(:wsgi_file_name, 'main.wsgi')
      execute "ln -sf #{wsgi_path}/#{wsgi_file_name} #{wsgi_path}/live.wsgi"
    end
  end

  desc "Generate migrations"
  task :makemigrations do
      django('makemigrations')
  end

  desc "Run django migrations"
  task :migrate do
    if fetch(:multidb)
      django("sync_all", '--noinput', run_on=:web)
    else
      django("migrate", "--noinput", run_on=:web)
    end
  end
end

namespace :python do
    def virtualenv_path
        if fetch(:use_pyenv)
          venv_name = "#{fetch(:application)}-#{fetch(:python_version)}"
          "~/.pyenv/versions/#{venv_name}"
        else
          File.join(
              fetch(:shared_virtualenv) ? shared_path : release_path, "virtualenv"
          )
        end
    end
    
    def check_python
      installed = false
      on roles(:all) do
        if fetch(:use_pyenv)
            versions = capture 'pyenv', 'versions'
            versions.gsub!(' ', '')
            versions.gsub!('*', '')
            versions = versions.split('\n')
            installed = versions.includes? fetch(:python_version)
        else
            version = capture(:python, '-V')
            installed = version.split(' ')[1] == fetch(:python_version)
        end
      end
      installed
    end


    desc "Install python version"
    task :install_python do
      on roles(:all) do
        unless check_python
          if fetch(:use_pyenv)
            execute :pyenv, 'install', fetch(:python_version)
          else
            python_file = "Python-#{fetch(:python_version)}.tgz"
            puts python_file
            source_path = "https://www.python.org/ftp/python/#{fetch(:python_version)}/#{python_file}"
            within shared_path do
              execute :wget, source_path
              execute :tar, '-zxf', "#{python_file}"
            end
            within "#{shared_path}/Python-#{fetch(:python_version)}" do
              with lc_all: :C do
                execute './configure', "--prefix=#{shared_path}/python_bin"
                execute 'make'
                execute 'make', 'install'
              end
            end
            within "#{shared_path}" do
              execute :rm, "Python-#{fetch(:python_version)}.tgz"
              execute :rm, '-rf', "#{shared_path}/Python-#{fetch(:python_version)}"
              unless File.exist?('python_bin/bin/python')
                execute(
                  :ln, '-s', File.join(shared_path, 'python_bin/bin/python3'), File.join(shared_path, 'python_bin/bin/python')
                )
              end
              unless File.exist?('python_bin/bin/pip')
                execute(
                  :ln, '-s', File.join(shared_path, 'python_bin/bin/pip3'), File.join(shared_path, 'python_bin/bin/pip')
                )
              end
            end
          end
        end
      end
    end

    desc "Create a python virtualenv"
    task :create_virtualenv do
        on roles(:all) do
            if fetch(:use_pyenv)
              unless File.directory?(virtualenv_path)
                venv_name = "#{fetch(:application)}-#{fetch(:python_version)}"
                with lc_all: :C do
                  execute "pyenv virtualenv #{fetch(:python_version)} #{venv_name}"
                end
              end
              with lc_all: :C do
                execute "#{virtualenv_path}/bin/pip install --upgrade pip"
                execute "#{virtualenv_path}/bin/pip install -r #{release_path}/#{fetch(:pip_requirements)}"
              end
            else
              if check_python
                execute "virtualenv", "#{virtualenv_path}"
                with lc_all: :C do
                  execute "#{virtualenv_path}/bin/pip install --upgrade pip"
                  execute "#{virtualenv_path}/bin/pip", "install", "-r", "#{release_path}/#{fetch(:pip_requirements)}"
                end
              else
                if capture("ls #{shared_path}").split().include?('python_bin')
                  puts "Python already installed"
                else
                  invoke 'python:install_python'
                end
                if capture("ls #{shared_path}").split().include?('virtualenv')
                  if fetch(:use_celery)
                    invoke 'django:stop_celery'
                  end
                else
                  execute "virtualenv -p #{shared_path}/python_bin/bin/python #{virtualenv_path}"
                  with lc_all: :C do
                    execute "#{virtualenv_path}/bin/pip install --upgrade pip"    
                    execute "#{virtualenv_path}/bin/pip install -r #{release_path}/#{fetch(:pip_requirements)}"    
                  end
                end
                
              end
            end
            
            if fetch(:shared_virtualenv) || fetch(:use_pyenv)
              execute :ln, "-s", virtualenv_path, File.join(release_path, 'virtualenv')
            end
        end
      if fetch(:npm_tasks)
        invoke 'nodejs:npm'
      end
      
      if fetch(:flask)
        invoke 'flask:setup'
      else
        invoke 'django:setup'
      end
    end

    
  # end
end


