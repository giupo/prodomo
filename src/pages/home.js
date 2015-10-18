import app from 'ampersand-app';
import React from 'react';

export default React.createClass({
  displayName : 'HomePage',

  onLogoutClick (event) {
    event.preventDefault();
    app.router.history.navigate('/logout');
  },

  render () {
    console.log("HomePage called")
    return  (
        <div className='container'>
          <header role='banner'>
            <h1>Labelr</h1>
          </header>
          <div>
           <p>We label stuff for you, beacuse, we can &trade;</p>
              <a href='/logout' onClick={this.onLogoutClick} className='button button-large'>
                <span className='mega octicon octicon-mark-github'></span> Logged in with Github
              </a>
          </div>
        </div>
    );
  }
});
