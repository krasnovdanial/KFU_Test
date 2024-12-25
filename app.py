from flask import Flask, render_template, request, jsonify
from models import db, Operator, Well, Production, Equipment, Maintenance
from forms import FilterForm
from datetime import date
import secrets

# Генерация 32-байтового секретного ключа в шестнадцатеричном формате
secret_key = secrets.token_hex(32)
app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key  # Замените на ваш секретный ключ
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///oil.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_request
def create_tables():
    db.create_all()
    populate_data()

def populate_data():
    # Проверяем, заполнены ли уже таблицы
    if Operator.query.first():
        return

    # Добавляем операторы
    operator1 = Operator(name='Оператор A', country='США')
    operator2 = Operator(name='Оператор B', country='Россия')
    db.session.add_all([operator1, operator2])
    db.session.commit()

    # Добавляем скважины
    well1 = Well(name='Скважины 1', location='Локация X', status='active', operator=operator1)
    well2 = Well(name='Скважины 2', location='Локация Y', status='inactive', operator=operator1)
    well3 = Well(name='Скважины 3', location='Локация Z', status='active', operator=operator2)
    db.session.add_all([well1, well2, well3])
    db.session.commit()

    # Добавляем производство
    production1 = Production(well=well1, date=date(2023, 1, 1), oil_produced=1000.0, gas_produced=500.0)
    production2 = Production(well=well1, date=date(2023, 2, 1), oil_produced=1100.0, gas_produced=550.0)
    production3 = Production(well=well2, date=date(2023, 1, 15), oil_produced=800.0, gas_produced=400.0)
    production4 = Production(well=well3, date=date(2023, 3, 1), oil_produced=1200.0, gas_produced=600.0)
    db.session.add_all([production1, production2, production3, production4])
    db.session.commit()

    # Добавляем оборудование
    equipment1 = Equipment(name='Насос A', type='Насос', well=well1)
    equipment2 = Equipment(name='Клапан B', type='Клапан', well=well1)
    equipment3 = Equipment(name='Насос C', type='Насос', well=well2)
    db.session.add_all([equipment1, equipment2, equipment3])
    db.session.commit()

    # Добавляем техобслуживание
    maintenance1 = Maintenance(equipment=equipment1, date=date(2023, 1, 10), description='Замененное уплотнение', cost=500.0)
    maintenance2 = Maintenance(equipment=equipment2, date=date(2023, 2, 20), description='Смазанный клапан', cost=200.0)
    maintenance3 = Maintenance(equipment=equipment3, date=date(2023, 3, 15), description='Обслуживание насоса', cost=300.0)
    db.session.add_all([maintenance1, maintenance2, maintenance3])
    db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    form = FilterForm()
    # Заполняем выбор операторов
    form.operator.choices = [('', 'Любой')] + [(str(op.id), op.name) for op in Operator.query.all()]

    if form.validate_on_submit():
        # Получаем фильтры
        operator_id = form.operator.data
        location = form.location.data
        well_status = form.well_status.data

        # Строим запрос
        query = Well.query
        if operator_id:
            query = query.filter_by(operator_id=int(operator_id))
        if location:
            query = query.filter(Well.location.ilike(f'%{location}%'))
        if well_status:
            query = query.filter_by(status=well_status)

        wells = query.all()

        # Формируем результат
        result = []
        for well in wells:
            well_data = {
                'id': well.id,
                'name': well.name,
                'location': well.location,
                'status': well.status,
                'operator': {
                    'id': well.operator.id,
                    'name': well.operator.name,
                    'country': well.operator.country
                },
                'productions': [
                    {
                        'id': prod.id,
                        'date': prod.date.isoformat(),
                        'oil_produced': prod.oil_produced,
                        'gas_produced': prod.gas_produced
                    } for prod in well.productions
                ],
                'equipments': [
                    {
                        'id': eq.id,
                        'name': eq.name,
                        'type': eq.type,
                        'maintenances': [
                            {
                                'id': maint.id,
                                'date': maint.date.isoformat(),
                                'description': maint.description,
                                'cost': maint.cost
                            } for maint in eq.maintenances
                        ]
                    } for eq in well.equipments
                ]

            }
            result.append(well_data)

        return jsonify(result)

    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
