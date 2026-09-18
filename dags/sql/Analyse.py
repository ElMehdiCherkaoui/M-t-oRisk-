from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from dags.sql.create_table import WeatherRiskGold

engine = create_engine('postgresql://postgres:postgres@127.0.0.1:5433/mydatabase')

SessionLocal = sessionmaker(bind=engine)

session = SessionLocal()


try:
    weather_risk_gold = session.query(WeatherRiskGold).filter(WeatherRiskGold.temperature_category == 'High Risk Heat').all()
    
    for record in weather_risk_gold:
        print(f"City: {record.city}, Date: {record.forecast_date}, Risk Score: {record.risk_score}, Temperature Category: {record.temperature_category}")
finally:
    session.close()
        
        
try:
    weather_risk_gold = session.query(WeatherRiskGold).filter(WeatherRiskGold.rain_category == 'High Risk Rain').all()
    print("Records with High Risk Probability in Rain Category:")
    for record in weather_risk_gold:
        print(f"City: {record.city}, Date: {record.forecast_date}, Risk Score: {record.risk_score}, Rain Category: {record.rain_category}")
finally:
    session.close()


try:
    results = session.query(WeatherRiskGold.city,func.avg(WeatherRiskGold.risk_score).label('avg_risk_score')).group_by(WeatherRiskGold.city).order_by(func.avg(WeatherRiskGold.risk_score).desc()).all()
    print("Cities with the highest average risk score:")
    for record in results:
        print(f"City: {record.city}, Average Risk Score: {record.avg_risk_score}")
finally:
    session.close()
    
try:
    period_max_risk = session.query(
        WeatherRiskGold.forecast_date, func.max(
            WeatherRiskGold.risk_score
            ).label('max_risk_score')
        ).group_by(
            WeatherRiskGold.forecast_date
            ).all()
    print("Periods with the highest risk score:")
    for record in period_max_risk:
        print(f"Date: {record.forecast_date}, Max Risk Score: {record.max_risk_score}")
        
finally:
    session.close()


try:
    ville_period_risk = session.query(
        WeatherRiskGold.city, WeatherRiskGold.forecast_date, func.max(WeatherRiskGold.risk_score).label('max_risk_score')
        ).group_by(
            WeatherRiskGold.city,
            WeatherRiskGold.forecast_date
            ).all()
    
    
    
    for record in ville_period_risk:
        print(f"City: {record.city}, Date: {record.forecast_date}, Max Risk Score: {record.max_risk_score}")
finally:
    session.close()


try:
    number_total_city = session.query(WeatherRiskGold.city).group_by(WeatherRiskGold.city).count()
    print(f"Total number of distinct cities: {number_total_city}")
finally:
    session.close()

try:
    max_temp = session.query(func.max(WeatherRiskGold.temp_max)).first()
    print(f"Maximum temperature: {max_temp}")
finally:
    session.close()
    
try:
    precipitation_max = session.query(func.max(WeatherRiskGold.precipitation)).first()
    print(f"Maximum precipitation: {precipitation_max}")
finally:
    session.close()