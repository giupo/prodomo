import app from 'ampersand-app';
import styles from './styles/main.styl';
import 'octicons/octicons/octicons.css';
import Router from './router';

// exposes `app` for console usage

window.app = app;

app.extend({
    init() {
        console.log('app starting');
        this.router = new Router();
        this.router.history.start({pushState: true});
        this.trigger('AppInit', 'ciula');
    }
});

app.on('AppInit', (data)=> {
  console.log('App started ' + data);
});

app.on('hello', (data) => {
  console.log(data);
});

app.init();
