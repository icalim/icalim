import pyupbit
import numpy as np

#OHLCV(Open, High, Low, Close, Volume)로 당일 시가, 고가, 저가, 종가, 거래량

df = pyupbit.get_ohlcv("KRW-SAND", count = 14)

#변동폭 * k 계산, (고가 - 저가) * k값
df['range'] = (df['high'] - df['low']) * 0.6

#target(매수가), range 컬럼을 한칸씩 아래로 내림(.shift(1))
df['target'] = df['open'] + df['range'].shift(1)

print(df)

#ror(수익율), np.where(조건문, 참일때 값, 거짓일때 값) : np.where = NumPy 라이브러리 활용
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'],
                     1)
#누적 곱 계산(cumprod) => 누적 수익율
df['hpr'] = df['ror'].cumprod()

#Draw Down 계산 (누적 최대값과 현재 hpr 차이 / 누적 최대값 * 100)
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
print("MDD(%): ", df['dd'].max())

#엑셀로 출력
df.to_excel("01.xlsx")
