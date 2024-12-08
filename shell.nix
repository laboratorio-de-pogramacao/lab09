{ pkgs ? import <nixpkgs> {} }:

let
    pythonEnv = pkgs.python3.withPackages (ps: with ps; [ pip ]);
in
pkgs.mkShell {
    buildInputs = [ pythonEnv ] ++ (with pkgs; [
        tree
        firefox
        geckodriver # Selenium driver
    ]);


    shellHook = ''
        export PYTHONPATH=$PYTHONPATH:$(pwd)

        python3 -m venv .venv
        source .venv/bin/activate

        pip install --upgrade pip
        pip install -r requirements.txt

        alias cls='clear'
        alias dbuild='docker build -t jenkins-python .'
        alias drun='docker run --name jenkins-python-container -p 8080:8080 -p 50000:50000 -v jenkins_data:/var/jenkins_home jenkins-python'
        alias makemigrations='python manage.py makemigrations '
        alias sqlmigrate='python manage.py sqlmigrate topics 0001'
        alias migrate='python manage.py migrate'
        alias updatedb='makemigrations; sqlmigrate; migrate'
        alias runserver='cd mysite; python manage.py runserver; cd ..'
        alias open='firefox "http://127.0.0.1:8000/topics"'
        alias test='cd mysite; python manage.py test; cd ..'
        alias run='open; runserver'
    '';
}