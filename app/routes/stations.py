from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import FuelStation

bp = Blueprint('stations', __name__, url_prefix='/stations')


@bp.route('/')
@login_required
def index():
    """List all fuel stations"""
    stations = FuelStation.query.filter_by(user_id=current_user.id).order_by(
        FuelStation.is_favorite.desc(),
        FuelStation.times_used.desc()
    ).all()

    return render_template('stations/index.html', stations=stations)


@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    """Add a new fuel station"""
    if request.method == 'POST':
        station = FuelStation(
            user_id=current_user.id,
            name=request.form.get('name'),
            brand=request.form.get('brand'),
            address=request.form.get('address'),
            city=request.form.get('city'),
            postcode=request.form.get('postcode'),
            notes=request.form.get('notes'),
            is_favorite=request.form.get('is_favorite') == 'on',
        )

        # Optional coordinates
        if request.form.get('latitude'):
            station.latitude = float(request.form.get('latitude'))
        if request.form.get('longitude'):
            station.longitude = float(request.form.get('longitude'))

        db.session.add(station)
        db.session.commit()

        flash(f'Station "{station.name}" added', 'success')
        return redirect(url_for('stations.index'))

    return render_template('stations/form.html', station=None)


@bp.route('/<int:station_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(station_id):
    """Edit a fuel station"""
    station = FuelStation.query.get_or_404(station_id)

    if station.user_id != current_user.id:
        flash('Access denied', 'error')
        return redirect(url_for('stations.index'))

    if request.method == 'POST':
        station.name = request.form.get('name')
        station.brand = request.form.get('brand')
        station.address = request.form.get('address')
        station.city = request.form.get('city')
        station.postcode = request.form.get('postcode')
        station.notes = request.form.get('notes')
        station.is_favorite = request.form.get('is_favorite') == 'on'

        if request.form.get('latitude'):
            station.latitude = float(request.form.get('latitude'))
        else:
            station.latitude = None
        if request.form.get('longitude'):
            station.longitude = float(request.form.get('longitude'))
        else:
            station.longitude = None

        db.session.commit()
        flash('Station updated', 'success')
        return redirect(url_for('stations.index'))

    return render_template('stations/form.html', station=station)


@bp.route('/<int:station_id>/favorite', methods=['POST'])
@login_required
def toggle_favorite(station_id):
    """Toggle favorite status"""
    station = FuelStation.query.get_or_404(station_id)

    if station.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Access denied'}), 403

    station.is_favorite = not station.is_favorite
    db.session.commit()

    return jsonify({'success': True, 'is_favorite': station.is_favorite})


@bp.route('/<int:station_id>/delete', methods=['POST'])
@login_required
def delete(station_id):
    """Delete a fuel station"""
    station = FuelStation.query.get_or_404(station_id)

    if station.user_id != current_user.id:
        flash('Access denied', 'error')
        return redirect(url_for('stations.index'))

    name = station.name
    db.session.delete(station)
    db.session.commit()

    flash(f'Station "{name}" deleted', 'success')
    return redirect(url_for('stations.index'))


@bp.route('/api/list')
@login_required
def api_list():
    """Get list of stations for autocomplete/selection"""
    stations = FuelStation.query.filter_by(user_id=current_user.id).order_by(
        FuelStation.is_favorite.desc(),
        FuelStation.times_used.desc()
    ).all()

    return jsonify([{
        'id': s.id,
        'name': s.name,
        'brand': s.brand,
        'address': s.address,
        'is_favorite': s.is_favorite
    } for s in stations])
