
$(function(){

    var Todo = Backbone.Model.extend({

        defaults: function() {
            return {
                title: "empty todo",
                prio:  Todos.nextPrio(),
                done: false
            };
        },

        initialize: function() {
            if (!this.get("title")) {
                this.set({"title": this.defaults().title});
            }
        },

        toggle: function() {
            this.save({done: !this.get("done")});
        }

    });

    var TodoList = Backbone.Collection.extend({

        model: Todo,

        done: function() {
            return this.filter(function(todo){return todo.get('done'); });
        },

        remaining: function() {
            return this.without.apply(this, this.done());
        },

        nextPrio: function() {
            if (!this.length) return 1;
            return this.last().get('prio') + 1;
        },

        comparator: function(todo) {
            return todo.get('prio');
        },

        url: '/todos'

    });

    var Todos = new TodoList;

    var TodoView = Backbone.View.extend({

        tagName: "li",

        className: "draggable",

        template: _.template($('#item-template').html()),

        events: {
            "click .toggle"   : "toggleDone",
            "dblclick .view"  : "edit",
            "click a.destroy" : "clear",
            "keypress .edit"  : "updateOnEnter",
            "blur .edit"      : "close",
            "drop"            : "drop"
        },

        initialize: function() {
            this.listenTo(this.model, 'change', this.render);
            this.listenTo(this.model, 'destroy', this.remove);
        },

        drop: function(event, index) {
            this.$el.trigger('update-sort', [this.model, index]);
        },

        render: function() {
            this.$el.html(this.template(this.model.toJSON()));
            this.$el.toggleClass('done', this.model.get('done'));
            this.input = this.$('.edit');
            return this;
        },

        toggleDone: function() {
            this.model.toggle();
        },

        edit: function() {
            this.$el.addClass("editing");
            this.input.focus();
        },

        close: function() {
            var value = this.input.val();
            if (!value) {
                this.clear();
            } else {
                this.model.save({title: value});
                this.$el.removeClass("editing");
            }
        },

        updateOnEnter: function(e) {
            if (e.keyCode == 13) this.close();
        },

        clear: function() {
            this.model.destroy();
        }

    });

    var AppView = Backbone.View.extend({

        el: $("#todoapp"),

        statsTemplate: _.template($('#stats-template').html()),

        events: {
            "keypress #new-todo"       : "createOnEnter",
            "keypress #new-todo-button": "create",
            "click #clear-all"         : "clearAll",
            "click #toggle-all"        : "toggleAllComplete",
            "update-sort"              : "updateSort"
        },

        initialize: function() {
            this.input = this.$("#new-todo");
            this.allCheckbox = this.$("#toggle-all")[0];

            this.listenTo(Todos, 'add', this.addOne);
            this.listenTo(Todos, 'reset', this.addAll);
            this.listenTo(Todos, 'all', this.render);

            this.footer = this.$('footer');
            this.main = $('#main');

            Todos.fetch();
        },

        render: function() {
            var done = Todos.done().length;
            var remaining = Todos.remaining().length;

            if (Todos.length) {
                this.main.show();
                this.footer.show();
                this.footer.html(this.statsTemplate({done: done, remaining: remaining}));

//                this.$el.children().remove();
//                this.collection.each(this.appendModelView, this);
            } else {
                this.main.hide();
                this.footer.hide();
            }
            return this;
        },

        appendModelView: function(model) {
            var el = new Application.View.Item({model: model}).render().el;
            this.$el.append(el);
        },

        addOne: function(todo) {
            var view = new TodoView({model: todo});
            this.$("#todo-list").append(view.render().el);
        },

        addAll: function() {
            Todos.each(this.addOne, this);
        },

        createOnEnter: function(e) {
            if (e.keyCode != 13) return;
            if (!this.input.val()) return;

            this.create(e)
        },

        create: function(e) {
            if (!this.input.val()) return;
            Todos.create({title: this.input.val()});

            this.input.val('');
        },

        clearAll: function() {
            //var done = this.allCheckbox.checked;
            Todos.each(function (todo) {todo.save({'done': true}); });
            //_.invoke(Todos.done(), 'destroy');
            return false;
        },

        toggleAllComplete: function() {
            var done = this.allCheckbox.checked;
            Todos.each(function (todo) {todo.save({'done': done}); });
        },

        updateSort: function(event, model, position) {
            this.collection.remove(model);

            this.collection.each(function (model, index) {
                var ordinal = index;
                if (index >= position)
                    ordinal += 1;
                model.set('ordinal', ordinal);
            });
            model.set('ordinal', position);
            this.collection.add(model, {at: position});

            // to update ordinals on server:
            var ids = this.collection.pluck('id');
            $('#post-data').html('post ids to server: ' + ids.join(', '));
            this.render();
        }
    });

    var App = new AppView;

    $('#todo-list').sortable({
        stop: function(event, ui) {
            ui.item.trigger('drop', ui.item.index());
        }
    });

});
