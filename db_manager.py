from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Конфігурація бази даних
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bus_station.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Моделі бази даних
class Bus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    route_number = db.Column(db.String(50), nullable=False)
    departure_time = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(100), nullable=False)

class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    license_number = db.Column(db.String(50), nullable=False)

class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_point = db.Column(db.String(100), nullable=False)
    end_point = db.Column(db.String(100), nullable=False)
    distance_km = db.Column(db.Float, nullable=False)

class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bus_id = db.Column(db.Integer, db.ForeignKey('bus.id'), nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'), nullable=False)
    departure_time = db.Column(db.String(50), nullable=False)
    arrival_time = db.Column(db.String(50), nullable=False)

    bus = db.relationship('Bus', backref='schedules')
    route = db.relationship('Route', backref='schedules')

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    passenger_name = db.Column(db.String(100), nullable=False)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedule.id'), nullable=False)
    seat_number = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float, nullable=False)

    schedule = db.relationship('Schedule', backref='tickets')

# Головна сторінка
@app.route('/')
def index():
    tables = ['Bus', 'Driver', 'Route', 'Schedule', 'Ticket']
    return render_template('index.html', tables=tables)

# Відображення записів із таблиці
@app.route('/table/<string:table_name>')
def show_table(table_name):
    if table_name == 'Bus':
        records = Bus.query.all()
    elif table_name == 'Driver':
        records = Driver.query.all()
    elif table_name == 'Route':
        records = Route.query.all()
    elif table_name == 'Schedule':
        records = Schedule.query.all()
    elif table_name == 'Ticket':
        records = Ticket.query.all()
    else:
        return "Table not found", 404
    return render_template('table.html', table_name=table_name, records=records)

# Додавання запису
@app.route('/add/<string:table_name>', methods=['GET', 'POST'])
def add_record(table_name):
    if request.method == 'POST':
        if table_name == 'Bus':
            new_record = Bus(
                route_number=request.form['route_number'],
                departure_time=request.form['departure_time'],
                destination=request.form['destination']
            )
        elif table_name == 'Driver':
            new_record = Driver(
                name=request.form['name'],
                phone=request.form['phone'],
                license_number=request.form['license_number']
            )
        elif table_name == 'Route':
            new_record = Route(
                start_point=request.form['start_point'],
                end_point=request.form['end_point'],
                distance_km=request.form['distance_km']
            )
        elif table_name == 'Schedule':
            new_record = Schedule(
                bus_id=request.form['bus_id'],
                route_id=request.form['route_id'],
                departure_time=request.form['departure_time'],
                arrival_time=request.form['arrival_time']
            )
        elif table_name == 'Ticket':
            new_record = Ticket(
                passenger_name=request.form['passenger_name'],
                schedule_id=request.form['schedule_id'],
                seat_number=request.form['seat_number'],
                price=request.form['price']
            )
        else:
            return "Table not found", 404
        db.session.add(new_record)
        db.session.commit()
        return redirect(url_for('show_table', table_name=table_name))
    return render_template('add.html', table_name=table_name)

# Редагування запису
@app.route('/edit/<string:table_name>/<int:record_id>', methods=['GET', 'POST'])
def edit_record(table_name, record_id):
    if table_name == 'Bus':
        record = Bus.query.get_or_404(record_id)
    elif table_name == 'Driver':
        record = Driver.query.get_or_404(record_id)
    elif table_name == 'Route':
        record = Route.query.get_or_404(record_id)
    elif table_name == 'Schedule':
        record = Schedule.query.get_or_404(record_id)
    elif table_name == 'Ticket':
        record = Ticket.query.get_or_404(record_id)
    else:
        return "Table not found", 404

    if request.method == 'POST':
        if table_name == 'Bus':
            record.route_number = request.form['route_number']
            record.departure_time = request.form['departure_time']
            record.destination = request.form['destination']
        elif table_name == 'Driver':
            record.name = request.form['name']
            record.phone = request.form['phone']
            record.license_number = request.form['license_number']
        elif table_name == 'Route':
            record.start_point = request.form['start_point']
            record.end_point = request.form['end_point']
            record.distance_km = request.form['distance_km']
        elif table_name == 'Schedule':
            record.bus_id = request.form['bus_id']
            record.route_id = request.form['route_id']
            record.departure_time = request.form['departure_time']
            record.arrival_time = request.form['arrival_time']
        elif table_name == 'Ticket':
            record.passenger_name = request.form['passenger_name']
            record.schedule_id = request.form['schedule_id']
            record.seat_number = request.form['seat_number']
            record.price = request.form['price']
        db.session.commit()
        return redirect(url_for('show_table', table_name=table_name))
    return render_template('edit.html', table_name=table_name, record=record)

# Видалення запису
@app.route('/delete/<string:table_name>/<int:record_id>', methods=['POST'])
def delete_record(table_name, record_id):
    if table_name == 'Bus':
        record = Bus.query.get_or_404(record_id)
    elif table_name == 'Driver':
        record = Driver.query.get_or_404(record_id)
    elif table_name == 'Route':
        record = Route.query.get_or_404(record_id)
    elif table_name == 'Schedule':
        record = Schedule.query.get_or_404(record_id)
    elif table_name == 'Ticket':
        record = Ticket.query.get_or_404(record_id)
    else:
        return "Table not found", 404
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for('show_table', table_name=table_name))


if __name__ == '__main__':
    # Ініціалізація бази даних
    with app.app_context():
        db.create_all()

    # Запуск програми
    app.run(debug=True)
