from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify

doc = Blueprint('doc', __name__, template_folder= 'templates', static_folder= 'static')
