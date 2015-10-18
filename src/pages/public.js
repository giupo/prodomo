import app from 'ampersand-app';
import React from 'react';

export default React.createClass({
  displayName : 'PublicPage',

  onLoginClick (event) {
    event.preventDefault();
    app.router.history.navigate('/login');
  },

  render () {
    console.log("PublicPage called")
    return  (
        <div className='container'>
          <header role='banner'>
            <h1>Labelr</h1>
          </header>
          <div>
           <p>We label stuff for you, beacuse, we can &trade;</p>
              <a href='/login' onClick={this.onLoginClick} className='button button-large'>
                <span className='mega octicon octicon-mark-github'></span> Login with Github
              </a>
          </div>
        </div>
    );
  }
});
