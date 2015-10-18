import app from 'ampersand-app';
import Router from 'ampersand-router';
import PublicPage from './pages/public';
import ReposPage from './pages/repos';
import PippoPage from './pages/pippo';
import React from 'react';
import ReactDom from 'react-dom'
import HomePage from './pages/home';

export default Router.extend({
  routes: {
    '': 'public',
    'repos': 'repos',
    'otherpage': 'otherpage',
    'login' : 'login',
    'logout' : 'logout'
	},

  public () {
    app.trigger('hello', {data:'ciccio'});
    ReactDom.render(<PublicPage/>, document.body);
  },

  repos () {
    ReactDom.render(<ReposPage/>, document.body);
  },

  otherpage() {
    ReactDom.render(<PippoPage/>, document.body);
  },

  login() {
    console.log("Router::login called");
    ReactDom.render(<HomePage/>, document.body);
  },

  logout() {
    app.router.history.navigate('/');
  }
});
