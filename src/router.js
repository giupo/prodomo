'use strict';

/* jshint unused: false */

import app from 'ampersand-app';
import Router from 'ampersand-router';
import PublicPage from './pages/public';
import ReposPage from './pages/repos';
import PippoPage from './pages/pippo';
import React from 'react';
import ReactDom from 'react-dom';
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
    /* jshint ignore:start */
    ReactDom.render(<PublicPage/>, document.body);
    /* jshint ignore:end */
  },

  repos () {
    /* jshint ignore:start */
    ReactDom.render(<ReposPage/>, document.body);
    /* jshint ignore:end */
  },

  otherpage() {
    /* jshint ignore:start */
    ReactDom.render(<PippoPage/>, document.body);
    /* jshint ignore:end */
  },

  login() {
    console.log('Router::login called');
    /* jshint ignore:start */
    ReactDom.render(<HomePage/>, document.body);
    /* jshint ignore:end */
  },

  logout() {
    app.router.history.navigate('/');
  }
});
