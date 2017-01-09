#!/bin/bash

# install homebrew
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

brew install nodejs npm yarn
brew install gitbook-editor
brew install pandoc
brew install Caskroom/cask/calibre
npm install -g gitbook
