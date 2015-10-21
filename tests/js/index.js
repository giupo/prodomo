'use strict';

var test = require('tape');
var State = require('ampersand-state');

var Person = State.extend({
    props: {
        name: 'string'
    }
});

test('init with values', function (t) {
    var person = new Person({name: 'henrik'});
    t.ok(person);
    t.equal(person.name, 'henrik');
    t.end();
});

test('after init, change should be empty until a set op', function (t) {
    var person = new Person({name: 'phil'});
    t.deepEqual(person._changed, {});
    t.notOk(person.changedAttributes());
    t.end();
});
