__author__ = 'Ethan'

from xlsxwriter import Workbook
from data.data import *
from data.parameters import DUT_NAME, DUT_TYPE, RADIO, STA_TYPE, ANGLE_NUM, LINE_LOSS, RUN_TPYE, ADAPTER, SERVER_SCRIPT, CLIENT_SCRIPT, PAIR, DURATION
import time

now_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
stop_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
if RUN_TPYE == 0:
    test_type = '_OTA'
elif RUN_TPYE == 1:
    test_type = '_Conductive'
else:
    test_type = ''
filename = DUT_NAME + '_' + RADIO + '_' + STA_TYPE + '_Rate_vs_Range' + test_type + '_Test_Report_' + now_time + '.xlsx'
# print('Report:', filename)
workbook: Workbook = Workbook('./Report/' + filename)
worksheet_cover = workbook.add_worksheet("Overview")
worksheet_environment = workbook.add_worksheet("Environment")
worksheet_range = workbook.add_worksheet("Rate_vs_Range")
if ANGLE_NUM > 1:
    worksheet_angle = workbook.add_worksheet("Rate_vs_Angle")
    worksheet_angle.hide_gridlines(2)
worksheet_data = workbook.add_worksheet("Data")
worksheet_cover.hide_gridlines(2)
worksheet_environment.hide_gridlines(2)
worksheet_range.hide_gridlines(2)
worksheet_data.hide_gridlines(2)

# title
if ANGLE_NUM > 1:
    title = ['Channel', 'Path_Loss(dB)', 'Angle', 'DL_Throughput', 'DL_Throughput_avg', 'UL_Throughput',
             'UL_Throughput_avg', 'Sta_Rssi', 'Sta_Rssi_avg', 'AP_Rssi', 'AP_Rssi_avg', 'DL_Rate', 'DL_Rate_avg',
             'UL_Rate', 'UL_Rate_avg', 'Duration', 'BW(DL)', 'NSS(DL)', 'MCS(DL)', 'BW(UL)', 'NSS(UL)', 'MCS(UL)',
             'STA RSSI(per chain)', 'AP POWER', 'AP RSSI(per chain)', 'STA POWER']
else:
    title = ['Channel', 'Path_Loss(dB)', 'Angle', 'DL_Throughput', 'UL_Throughput', 'Sta_Rssi', 'AP_Rssi',
             'DL_Rate', 'UL_Rate', 'Duration', 'BW(DL)', 'NSS(DL)', 'MCS(DL)', 'BW(UL)', 'NSS(UL)', 'MCS(UL)',
             'STA RSSI(per chain)', 'AP POWER', 'AP RSSI(per chain)', 'STA POWER']

# 设置列宽
worksheet_cover.set_column('B:B', 12)
worksheet_cover.set_column('C:C', 26)
worksheet_cover.set_column('D:D', 35)
worksheet_cover.set_row(7, 35)

worksheet_data.set_column('A:A', 12)
worksheet_data.set_column('B:B', 20)
worksheet_data.set_column('C:C', 9)
worksheet_data.set_column('D:D', 22)
worksheet_data.set_column('E:E', 29)
worksheet_data.set_column('F:F', 22)
worksheet_data.set_column('G:G', 29)
worksheet_data.set_column('H:H', 13)
worksheet_data.set_column('I:I', 20)
worksheet_data.set_column('J:J', 13)
worksheet_data.set_column('K:K', 20)
worksheet_data.set_column('L:L', 13)
worksheet_data.set_column('M:M', 20)
worksheet_data.set_column('N:N', 13)
worksheet_data.set_column('O:O', 20)
worksheet_data.set_column('P:P', 8)
worksheet_data.set_column('Q:V', 12)
worksheet_data.set_column('W:W', 30)
worksheet_data.set_column('X:X', 18)
worksheet_data.set_column('Y:Y', 30)
worksheet_data.set_column('Z:Z', 18)
worksheet_data.set_row(0, 22)
for row in range(1, 100):
    worksheet_data.set_row(row, 16.5)

company_format = workbook.add_format({
    'align': 'left',
    'font_name': 'Arial Unicode MS',
})

report_name_format = workbook.add_format({
    'font_size': 28,
    'bold': True,
    'align': 'left',
    'font_name': 'Verdana',
})

info_format = workbook.add_format({
    'italic': True,
    'align': 'left',
    'font_name': 'Times New Roman',
})

head_format = workbook.add_format({
    'font_size': 14,
    'bold': True,
    'align': 'center',
    'valign': 'vcenter',
    'border': True,
    'bottom': 3,
    'top': 3,
    'left': 3,
    'right': 3,
    # 'fg_color': '#124191',
    'fg_color': '#00C9FF',
    'font_name': 'Arial Unicode MS',
})

merge_atten_format = workbook.add_format(
    {
        'font_size': 11,
        'bold': True,
        'border': True,
        'bottom': 3,
        'top': 3,
        'left': 3,
        'right': 3,
        'align': 'center',
        'valign': 'vcenter',
        # 'fg_color': '#00C9FF',
        'font_name': 'Arial Unicode MS',
    }
)

merge_channel_format = workbook.add_format(
    {
        'font_size': 11,
        'bold': True,
        'border': True,
        'bottom': 3,
        'top': 3,
        'left': 3,
        'right': 3,
        'align': 'center',
        'valign': 'vcenter',
        # 'fg_color': '#C5C1BB',
        'font_name': 'Arial Unicode MS',
    }
)

tp_format = workbook.add_format({
    'border': True,
    'bottom': 3,
    'top': 3,
    'left': 3,
    'right': 3,
    'num_format': '0.000',
    'font_name': 'Arial Unicode MS',
})

rssi_format = workbook.add_format({
    'border': True,
    'bottom': 3,
    'top': 3,
    'left': 3,
    'right': 3,
    'num_format': '0',
    'font_name': 'Arial Unicode MS',
})

rate_format = workbook.add_format({
    'border': True,
    'bottom': 3,
    'top': 3,
    'left': 3,
    'right': 3,
    'num_format': '0',
    'font_name': 'Arial Unicode MS',
})

data_format = workbook.add_format({
    'border': True,
    'bottom': 3,
    'top': 3,
    'left': 3,
    'right': 3,
    'font_name': 'Arial Unicode MS',
})

merge_format = workbook.add_format(
    {
        'font_size': 11,
        'border': True,
        'bottom': 3,
        'top': 3,
        'left': 3,
        'right': 3,
        'align': 'center',
        'valign': 'vcenter',
        'num_format': '0',
        'font_name': 'Arial Unicode MS',
    }
)

border_format = workbook.add_format(
    {
        'border': True,
        'bottom': 3,
        'top': 3,
        'left': 3,
        'right': 3,
    }
)


def write_row():
    att_num = Reportdata_Get.Att_get()
    border_range = ANGLE_NUM * int(len(att_num))
    for r in range(len(title)):
        for c in range(border_range + 1):
            worksheet_data.write(c, r, None, border_format)
    worksheet_data.write_row("A1", title, head_format)


def write_Channel():
    posX = ord('A')
    posY = 2
    posZ = posY + int(ANGLE_NUM) - 1
    for channel in Channel:
        if ANGLE_NUM > 1:
            worksheet_data.merge_range(str(chr(posX) + str(posY) + ":" + chr(posX) + str(posZ)), channel,
                                       merge_channel_format)
            posY += int(ANGLE_NUM)
            posZ += int(ANGLE_NUM)
        else:
            worksheet_data.write(chr(posX) + str(posY), channel, data_format)
            posY += 1


def write_Attenuation():
    posX = ord('B')
    posY = 2
    posZ = posY + int(ANGLE_NUM) - 1
    for attenvalue in Att_rep:
        attenvalue = attenvalue + LINE_LOSS
        if ANGLE_NUM > 1:
            worksheet_data.merge_range(str(chr(posX) + str(posY) + ":" + chr(posX) + str(posZ)), attenvalue,
                                       merge_atten_format)
            posY += int(ANGLE_NUM)
            posZ += int(ANGLE_NUM)
        else:
            worksheet_data.write(chr(posX) + str(posY), attenvalue, data_format)
            posY += 1


def write_Angle():
    posX = ord('C')
    posY = 2
    for angle in Angle:
        worksheet_data.write(chr(posX) + str(posY), angle, data_format)
        posY += 1


def write_Tx():
    posX = ord('D')
    posY = 2
    for tx in Tx_Throught:
        worksheet_data.write(chr(posX) + str(posY), tx, tp_format)
        posY += 1
    return posX


def write_Rx(posX=None):
    posX = posX + 1
    posY = 2
    for rx in Rx_Throught:
        worksheet_data.write(chr(posX) + str(posY), rx, tp_format)
        posY += 1
    return posX


def write_AP_Rssi(posX=None):
    posX = posX + 1
    posY = 2
    for aprssi in Ap_Rssi:
        worksheet_data.write(chr(posX) + str(posY), int(aprssi), rssi_format)
        posY += 1
    return posX


def write_STA_Rssi(posX=None):
    posX = posX + 1
    posY = 2
    for starssi in Sta_Rssi:
        worksheet_data.write(chr(posX) + str(posY), int(starssi), rssi_format)
        posY += 1
    return posX


def write_Tx_Rate(posX=None):
    posX = posX + 1
    posY = 2
    for txrate in Tx_Rate:
        worksheet_data.write(chr(posX) + str(posY), txrate, rate_format)
        posY += 1
    return posX


def write_Rx_Rate(posX=None):
    posX = posX + 1
    posY = 2
    for rxrate in Rx_Rate:
        worksheet_data.write(chr(posX) + str(posY), rxrate, rate_format)
        posY += 1
    return posX


def write_Time(posX=None):
    posX = posX + 1
    posY = 2
    for time in Dura_Time:
        worksheet_data.write(chr(posX) + str(posY), int(time), data_format)
        posY += 1
    return posX


def write_TX_MCS(posX=None):
    posX = posX + 1
    posY = 2
    for tx_mcs in MCS_Tx_Rate:
        worksheet_data.write(chr(posX) + str(posY), tx_mcs, data_format)
        posY += 1
    return posX


def write_TX_NSS(posX=None):
    posX = posX + 1
    posY = 2
    for tx_nss in NSS_Tx_Rate:
        worksheet_data.write(chr(posX) + str(posY), tx_nss, data_format)
        posY += 1
    return posX


def write_TX_BW(posX=None):
    posX = posX + 1
    posY = 2
    for tx_bw in BW_Tx_Rate:
        worksheet_data.write(chr(posX) + str(posY), tx_bw, data_format)
        posY += 1
    return posX


def write_RX_MCS(posX=None):
    posX = posX + 1
    posY = 2
    for rx_mcs in MCS_Rx_Rate:
        worksheet_data.write(chr(posX) + str(posY), rx_mcs, data_format)
        posY += 1
    return posX


def write_RX_NSS(posX=None):
    posX = posX + 1
    posY = 2
    for rx_nss in NSS_Rx_Rate:
        worksheet_data.write(chr(posX) + str(posY), rx_nss, data_format)
        posY += 1
    return posX


def write_RX_BW(posX=None):
    posX = posX + 1
    posY = 2
    for rx_bw in BW_Rx_Rate:
        worksheet_data.write(chr(posX) + str(posY), rx_bw, data_format)
        posY += 1
    return posX


def write_TX_ANTRSSI(posX=None):
    posX = posX + 1
    posY = 2
    for txant_rssi in TX_RSSI_ANT:
        worksheet_data.write(chr(posX) + str(posY), txant_rssi, data_format)
        posY += 1
    return posX


def write_TX_ANTPOWER(posX=None):
    posX = posX + 1
    posY = 2
    for txant_power in TX_POWER_ANT:
        worksheet_data.write(chr(posX) + str(posY), txant_power, data_format)
        posY += 1
    return posX


def write_RX_ANTRSSI(posX=None):
    posX = posX + 1
    posY = 2
    for rxant_rssi in RX_RSSI_ANT:
        worksheet_data.write(chr(posX) + str(posY), rxant_rssi, data_format)
        posY += 1
    return posX


def write_RX_ANTPOWER(posX=None):
    posX = posX + 1
    posY = 2
    for rxant_power in RX_POWER_ANT:
        worksheet_data.write(chr(posX) + str(posY), rxant_power, data_format)
        posY += 1
    return posX


# for average
def write_avg(posX=None):
    posXX = posX
    posX = posX + 1
    posY = 2
    posZ = posY + int(ANGLE_NUM) - 1
    for attenvalue in Att_rep:
        worksheet_data.merge_range(chr(posX) + str(posY) + ":" + chr(posX) + str(posZ), '', merge_format)
        worksheet_data.write_formula(chr(posX) + str(posY),
                                     '=AVERAGE(' + chr(posXX) + str(posY) + ':' + chr(posXX) + str(posZ) + ')',
                                     merge_format)
        posY += int(ANGLE_NUM)
        posZ += int(ANGLE_NUM)
    return posX


def write_range_att(posA, posB, posC, posX):
    chart = workbook.add_chart({"type": "line"})
    cur_row_axis = str(len(Att_rep) * int(ANGLE_NUM) + 1)
    chart.set_title(
        {
            "name": 'RVR'
        }
    )
    chart.set_y_axis(
        {
            "name": "Mbps",
            'major_gridlines': {'visible': False},
            'minor_gridlines': {'visible': False},
        }
    )
    chart.set_x_axis(
        {
            'name': 'Attenuation(dB)',
        }
    )

    chart.set_chartarea({
        'border': {'none': True},
        'fill': {'none': True},
        'gradient': {'colors': ['#00C9FF', '#124191']}
    })
    if ANGLE_NUM > 1:
        tptx_list_forrange = []
        att_list_forrange = []
        tprx_list_forrange = []
        posY = 2
        for att in Att_rep:
            tp_tx = 'Data!$' + chr(posA) + '$' + str(posY)
            tptx_list_forrange.append(tp_tx)
            tp_rx = 'Data!$' + chr(posC) + '$' + str(posY)
            tprx_list_forrange.append(tp_rx)
            att = 'Data!$' + chr(posB) + '$' + str(posY)
            att_list_forrange.append(att)
            posY += int(ANGLE_NUM)
        tptx_list_forrange = tuple(tptx_list_forrange)
        att_list_forrange = tuple(att_list_forrange)
        tprx_list_forrange = tuple(tprx_list_forrange)
        tptx_list_forrange = ','.join(tptx_list_forrange)
        att_list_forrange = ','.join(att_list_forrange)
        tprx_list_forrange = ','.join(tprx_list_forrange)
        tptx_list_forrange = str(tptx_list_forrange)
        att_list_forrange = str(att_list_forrange)
        tprx_list_forrange = str(tprx_list_forrange)
        chart.add_series({
            'name': 'DL Throughput',
            'categories': '=(' + att_list_forrange + ')',
            'values': '=(' + tptx_list_forrange + ')',
            'line': ({'color': '#FFFB00'}),
            'smooth': True,
            'gradient': {'colors': [ '#00C9FF', '#124191']},
            'marker': {
                'type': 'diamond',
                'size': 3,
                'border': {'color': 'red'},
                'fill': {'color': 'yellow'},
            },
        })
        chart.add_series({
            'name': 'UL Throughput',
            'categories': '=(' + att_list_forrange + ')',
            'values': '=(' + tprx_list_forrange + ')',
            'line': ({'color': '#4BDD33'}),
            'smooth': True,
            'gradient': {'colors': ['#00C9FF', '#124191']},
            'marker': {
                'type': 'circle',
                'size': 3,
                'border': {'color': 'red'},
                'fill': {'color': 'yellow'},
            },
        })
    else:
        chart.add_series({
            'name': 'DL Throughput',
            'categories': '=Data!$' + chr(posB) + '$2:$' + chr(posB) + '$' + cur_row_axis,
            'values': '=Data!$' + chr(posA) + '$2:$' + chr(posA) + '$' + cur_row_axis,
            'line': {'color': '#FFFB00'},
            'smooth': True,
            'marker': {
                'type': 'diamond',
                'size': 3,
                'border': {'color': 'red'},
                'fill': {'color': 'yellow'},
            },
        })
        chart.add_series({
            'name': 'UL Throughput',
            'categories': '=Data!$' + chr(posB) + '$2:$' + chr(posB) + '$' + cur_row_axis,
            'values': '=Data!$' + chr(posC) + '$2:$' + chr(posC) + '$' + cur_row_axis,
            'line': {'color': '#4BDD33'},
            'smooth': True,
            'marker': {
                'type': 'circle',
                'size': 3,
                'border': {'color': 'red'},
                'fill': {'color': 'yellow'},
            },
        })
    chart.set_plotarea({
        'border': {'none': True},
        'fill': {'none': False},
        # 'gradient': {'colors': ['#BBFFFF', '#AEEEEE', '#96CDCD']}
    })

    # chart.set_legend({'none': True})
    worksheet_range.insert_chart('B' + str(posX), chart, {'x_scale': 2.5, 'y_scale': 1.2})


def write_range(mode, posA, posB, posX):
    if mode == 'DL':
        name = 'DL Graph'
        tp_name = 'DL Throughput'
        chart = 'chart_tx'
        color_line = '#FFFB00'
        marker_type = 'diamond'
    elif mode == 'UL':
        name = 'UL Graph'
        tp_name = 'UL Throughput'
        chart = 'chart_rx'
        color_line = '#4BDD33'
        marker_type = 'circle'
    chart_tx = workbook.add_chart({"type": "line"})
    chart_rx = workbook.add_chart({"type": "line"})
    chart = eval(chart)
    # insert line graph
    cur_row_axis = str(len(Att_rep) * int(ANGLE_NUM) + 1)
    # cur_row_x = str(len(Att_rep) * int(ANGLE_NUM) + 1)
    # cur_row_chart = str(len(Att_rep) * int(ANGLE_NUM) + 2)
    chart.set_title(
        {
            "name": name
        }
    )
    chart.set_y_axis(
        {
            "name": "Mbps",
            'major_gridlines': {'visible': False},
            'minor_gridlines': {'visible': False},
        }
    )
    chart.set_x_axis(
        {
            'name': 'RSSI(dBm)',
        }
    )
    if mode == 'DL':
        chart.set_chartarea({
            'border': {'none': True},
            'fill': {'none': True},
            'gradient': {'colors': ['#87CEFA', '#00C9FF']}
        })
    else:
        chart.set_chartarea({
            'border': {'none': True},
            'fill': {'none': True},
            'gradient': {'colors': ['#87CEFA', '#124191']}
        })
    if ANGLE_NUM > 1:
        tp_list_forrange = []
        att_list_forrange = []
        posY = 2
        for att in Att_rep:
            tp = 'Data!$' + chr(posA) + '$' + str(posY)
            tp_list_forrange.append(tp)
            rssi = 'Data!$' + chr(posB) + '$' + str(posY)
            att_list_forrange.append(rssi)
            posY += int(ANGLE_NUM)
        tp_list_forrange = tuple(tp_list_forrange)
        att_list_forrange = tuple(att_list_forrange)
        tp_list_forrange = ','.join(tp_list_forrange)
        att_list_forrange = ','.join(att_list_forrange)
        tp_list_forrange = str(tp_list_forrange)
        att_list_forrange = str(att_list_forrange)
        chart.add_series({
            'name': tp_name,
            'categories': '=(' + att_list_forrange + ')',
            'values': '=(' + tp_list_forrange + ')',
            'line': ({'color': color_line}),
            'smooth': True,
            # 'gradient': {'colors': ['#FFE9D7', '#FFD4B2', '#FFC18B']},
            'marker': {
                'type': marker_type,
                'size': 3,
                'border': {'color': 'red'},
                'fill': {'color': 'yellow'},
            },
        })
    else:
        chart.add_series({
            'name': tp_name,
            'categories': '=Data!$' + chr(posB) + '$2:$' + chr(posB) + '$' + cur_row_axis,
            'values': '=Data!$' + chr(posA) + '$2:$' + chr(posA) + '$' + cur_row_axis,
            'line': {'color': color_line},
            'smooth': True,
            'marker': {
                'type': marker_type,
                'size': 3,
                'border': {'color': 'red'},
                'fill': {'color': 'yellow'},
            },
        })
    if mode == 'DL':
        chart.set_plotarea({
            'border': {'none': True},
            'fill': {'none': False},
            # 'gradient': {'colors': ['#FFE4CE', '#FFD4B2', '#FFC695']}
        })
    else:
        chart.set_plotarea({
            'border': {'none': True},
            'fill': {'none': False},
            # 'gradient': {'colors': ['#FFDBDB', '#FFC7C6', '#FFADAC']}
        })
    # chart.set_legend({'none': True})
    worksheet_range.insert_chart('B' + str(posX), chart, {'x_scale': 2.5, 'y_scale': 1.2})


def write_radar(posA, posE, max_tp=None):
    posB = ord('C')
    posY = 2
    posD = 2
    if posE == 'B':
        tp_type = 'DL Throughput'
        marker_type = 'circle'
        color_line = '#FFFB00'
    elif posE == 'J':
        tp_type = 'UL Throughput'
        marker_type = 'diamond'
        color_line = '#4BDD33'
    else:
        print('Check postion')
        pass
    for att in Att_rep:
        # insert line graph
        # radar = radar_name = 'radar' + str(att)
        radar = workbook.add_chart({"type": "radar"})
        # radar = eval(radar)
        radar.set_title({
            "name": 'Attenuation=' + str(att) + 'dB'
        })
        radar.set_y_axis({
            "name": "Mbps",
            "min": 0,
            "max": max_tp,
            "major_unit": max_tp // 8,
        })
        radar.set_x_axis(
            {
                'name': 'Angle'
            }
        )
        if posE == 'B':
            radar.set_chartarea({
                'border': {'none': True},
                'gradient': {'colors': ['#87CEFA', '#00C9FF']}
            })
        else:
            radar.set_chartarea({
                'border': {'none': True},
                'gradient': {'colors': ['#87CEFA', '#124191']}
            })
        if ANGLE_NUM > 1:
            radar.add_series({
                'name': tp_type,
                'categories': '=Data!$' + chr(posB) + '$' + str(posY) + ':$' + chr(posB) + '$' +
                              str(int(ANGLE_NUM) + posY - 1),
                'values': '=Data!$' + chr(posA) + '$' + str(posY) + ':$' + chr(posA) + '$' +
                          str(int(ANGLE_NUM) + posY - 1),
                'line': {'color': color_line},
                'smooth': True,
                # 'gradient': {'colors': ['#FFE9D7', '#FFD4B2', '#FFC18B']},
                'marker': {
                    'type': marker_type,
                    'size': 3,
                    'border': {'color': 'red'},
                    'fill': {'color': 'yellow'},
                },
            })
        else:
            pass
        if posE == 'B':
            radar.set_plotarea({
                'border': {'none': True},
                'fill': {'none': False},
                # 'gradient': {'colors': ['#E6DCF4', '#DED2F1', '#CBB8E9']}
            })
        else:
            radar.set_plotarea({
                'border': {'none': True},
                'fill': {'none': False},
                # 'gradient': {'colors': ['#DCF7FF', '#C3F1FF', '#A2EBFF']}
            })
        worksheet_angle.insert_chart(posE + str(posD), radar, {'x_scale': 1, 'y_scale': 1.4})
        posY += int(ANGLE_NUM)
        posD += 20


# add Auxiliary column
def addac_for_angle():
    worksheet_data.write_row('AA1', ['ac_for_angle'], head_format)
    posY = 2
    posYY = 2
    posYC = 0
    for angle in Angle:
        worksheet_data.write_formula('AA' + str(posY), '=$B$' + str(posYY) + '&"-"&C' + str(posY))
        posY += 1
        posYC += 1
        if posYC % 8 == 0:
            posYY += int(ANGLE_NUM)
    worksheet_data.set_column('AA:AA', None, None, {'hidden': True})


# def pivot_table(filename):
#     io = pd.ExcelFile('./Report/' + filename)
#     df = pd.read_excel(io, sheet_name='Data')
#     mydata = df.drop([0], axis=0)
#     table = pd.pivot_table(df, index=['ac_for_angle'], values=['Rx_Throughput', 'Tx_Throughput'])
#     table.to_excel(io, sheet_name='Rate_over_Angle')

def set_properties():
    workbook.set_properties({
        'title': 'WIFI Performance Test Report',
        'subject': 'WIFI TEST',
        'author': 'WiFiRF',
        'manager': 'BBD',
        'company': 'NSB',
        'category': 'Test Report',
        'keywords': 'RF, WIFI, Throughput',
        'comments': 'Created with Python and XlsxWriter'})


def book_close():
    workbook.close()


def Generate_Test_Report():
    dut_sn = hw_version = sw_version = None
    rep_to_excel = Reportdata_Get()
    try:
        rep_to_excel.Dutinfo_get()
    except:
        logger.error('No dutinfo')
    else:
        print(Dutinfo[0].split(',')[0])
        dut_sn = Dutinfo[0].split(',')[0]
        hw_version = Dutinfo[0].split(',')[1]
        sw_version = Dutinfo[0].split(',')[2]

    if STA_TYPE == 'AC88':
        sta_type = 'Wireless Card'
        sta_model = 'ASUS-AC88'
        sta_version = '1.558.48.8'
        op = '11ac'
        ant = '4x4'
    elif STA_TYPE == 'AX210':
        sta_type = 'Wireless Card'
        sta_model = 'Intel® AX210'
        sta_version = '22.170.0.3'
        op = '11ax'
        ant = '2x2'
    elif STA_TYPE == 'BE865':
        sta_type = 'Wireless Card'
        sta_model = 'Qualcomm® QCNCM865'
        sta_version = '3.1.0.1453'
        op = '11be'
        ant = '2x2'
    elif STA_TYPE == 'demo' or STA_TYPE == 'Demo' or STA_TYPE == 'DEMO':
        sta_type = 'QCA Demo'
        sta_model ='ipq95xx'
        sta_version = 'OpenWrt 19.07-SNAPSHOT'
        op = '11be'
        ant = '4x4'
    else:
        sta_type = ''
        sta_model = ''
        sta_version = ''
        op = ''
        ant = ''
    worksheet_cover.insert_image('A1', './images/NSB.png',{'x_offset':0.5,'y_offset':0,'x_scale':0.44,'y_scale':0.44,'positioning':1})
    # worksheet_cover.write_blank('B1', None)
    # worksheet_cover.set_header('&L&G', {'image_left': 'NSB.png'})
    # worksheet_cover.merge_range('B4:I4', 'NSB', company_format)
    worksheet_cover.merge_range('B5:I5', 'Respect Challenge Achievement Renewal', company_format)
    worksheet_cover.merge_range('B7:I7', 'WIFI Performance Test Report', report_name_format)
    # worksheet_cover.write('B9', 'StartTime', company_format)
    worksheet_cover.write('B10', 'Time', company_format)
    worksheet_cover.write('C10', stop_time, info_format)
    worksheet_cover.write('B12', 'DUT(AP)', company_format)
    worksheet_cover.write('C13', 'Product', company_format)
    worksheet_cover.write('D13', DUT_NAME, info_format)
    worksheet_cover.write('C14', 'SN', company_format)
    worksheet_cover.write('D14', dut_sn, info_format)
    worksheet_cover.write('C15', 'Hardware Version', company_format)
    worksheet_cover.write('D15', hw_version, info_format)
    worksheet_cover.write('C16', 'Software Version', company_format)
    worksheet_cover.write('D16', sw_version, info_format)
    worksheet_cover.write('C17', 'Operating Band', company_format)
    worksheet_cover.write('D17', RADIO, info_format)
    worksheet_cover.write('C18', 'Operation Mode', company_format)
    worksheet_cover.write('D18', op, info_format)
    worksheet_cover.write('C19', 'Antenna Configuration', company_format)
    worksheet_cover.write('D19', ant, info_format)
    
    worksheet_cover.write('B21', 'STATION', company_format)
    worksheet_cover.write('C21', 'Station Type', company_format)
    worksheet_cover.write('D21', sta_type, info_format)
    worksheet_cover.write('C22', 'Model', company_format)
    worksheet_cover.write('D22', sta_model, info_format)
    worksheet_cover.write('C23', 'Version', company_format)
    worksheet_cover.write('D23', sta_version, info_format)
    worksheet_cover.write('C24', 'Operating Band', company_format)
    worksheet_cover.write('D24', RADIO, info_format)
    worksheet_cover.write('C25', 'Operation Mode', company_format)
    worksheet_cover.write('D25', op, info_format)
    worksheet_cover.write('C26', 'Antenna Configuration', company_format)
    worksheet_cover.write('D26', ant, info_format)
    worksheet_cover.write('B29', 'TEST TOOLS', company_format)
    worksheet_cover.write('C30', 'Test Software', company_format)
    worksheet_cover.write('D30', 'iperf3', info_format)
    worksheet_cover.write('C31', 'Test Script', company_format)
    worksheet_cover.write('D31', 'iperf3 -s'+SERVER_SCRIPT+';'+'iperf3 -c Server ip -p Port -f m -V -J -t '+str(DURATION)+' -P '+str(PAIR)+' -S 0x08'+CLIENT_SCRIPT, info_format)

    worksheet_environment.write('B1', 'TEST DIAGRAM AND ENVIRONMENT', company_format)
    if RUN_TPYE == 0:
        try:
            worksheet_environment.insert_image('B3', './images/OTA.PNG')
        except:
            logger.error('No OTA Photo')
    else:
        try:
            worksheet_environment.insert_image('B3', './images/CDT.PNG')
        except:
            logger.error('No Conductive Photo')
    try:
        worksheet_environment.insert_image('M3', './images/tp.jpg')
    except:
        logger.error('No Environment Photo')
    else:
        try:
            worksheet_environment.insert_image('M3', './images/TP.PNG')
        except:
            logger.error('No Environment Photo')

    worksheet_range.write('V2', '***Note:Upstream and Downstream are based on Client***', info_format)
    if ANGLE_NUM > 1:
        worksheet_angle.write('S2', '***Note:Upstream and Downstream are based on Client***', info_format)
    
    try:
        rep_to_excel = Reportdata_Get()
    except:
        logger.error('No file')
    else:
        write_row()
        try:
            rep_to_excel.Ch_get()
            write_Channel()
        except:
            logger.error('No file')
        try:
            # rep_to_excel.Att_get()
            write_Attenuation()
        except:
            logger.error('No file')
        try:
            rep_to_excel.Angle_get()
            write_Angle()
        except:
            logger.error('No file')
        try:
            tx_tp = rep_to_excel.Tx_tp_get()
            posX = write_Tx()
            posX_txtp_avg = posX
        except:
            logger.error('No file')
            posX += 1
            posX_txtp_avg = posX
        if ANGLE_NUM > 1:
            posX = write_avg(posX)
            posX_txtp_avg = posX
        try:
            rx_tp = rep_to_excel.Rx_tp_get()
            posX = write_Rx(posX)
            posX_rxtp_avg = posX
        except:
            logger.error('No file')
            posX += 1
            posX_rxtp_avg = posX
        if ANGLE_NUM > 1:
            posX = write_avg(posX)
            posX_rxtp_avg = posX
        try:
            rep_to_excel.Sta_rssi_get()
            posX = write_STA_Rssi(posX)
            posX_STARSSI_avg = posX
        except:
            logger.error('No file')
            posX += 1
            posX_STARSSI_avg = posX
        if ANGLE_NUM > 1:
            posX = write_avg(posX)
            posX_STARSSI_avg = posX
        try:
            rep_to_excel.Ap_rssi_get()
            posX = write_AP_Rssi(posX)
            posX_APRSSI_avg = posX
        except:
            logger.error('No file')
            posX += 1
            posX_APRSSI_avg = posX
        if ANGLE_NUM > 1:
            posX = write_avg(posX)
            posX_APRSSI_avg = posX
        try:
            rep_to_excel.Tx_rate_get()
            posX = write_Tx_Rate(posX)
        except:
            logger.error('No file')
            posX += 1
        if ANGLE_NUM > 1:
            posX = write_avg(posX)
        try:
            rep_to_excel.Rx_rate_get()
            posX = write_Rx_Rate(posX)
        except:
            logger.error('No file')
            posX += 1
        if ANGLE_NUM > 1:
            posX = write_avg(posX)
        try:
            rep_to_excel.Dura_Time_get()
            posX = write_Time(posX)
        except:
            logger.error('No file')
            posX += 1
        try:
            rep_to_excel.BW_TxRate_get()
            posX = write_TX_BW(posX)
        except:
            logger.error('No file')
            posX += 1
        try:
            rep_to_excel.NSS_TxRate_get()
            posX = write_TX_NSS(posX)
        except:
            logger.error('No file')
            posX += 1
        try:
            rep_to_excel.MCS_TxRate_get()
            posX = write_TX_MCS(posX)
        except:
            logger.error('No file')
            posX += 1
        try:
            rep_to_excel.BW_RxRate_get()
            posX = write_RX_BW(posX)
        except:
            logger.error('No file')
            posX += 1
        try:
            rep_to_excel.NSS_RxRate_get()
            posX = write_RX_NSS(posX)
        except:
            logger.error('No file')
            posX += 1
        try:
            rep_to_excel.MCS_RxRate_get()
            posX = write_RX_MCS(posX)
        except:
            logger.error('No file')
            posX += 1
        try:
            rep_to_excel.RSSI_TXANT_get()
            posX = write_TX_ANTRSSI(posX)
        except:
            logger.error('No file')
            posX += 1
        try:
            rep_to_excel.POWER_TXANT_get()
            posX = write_TX_ANTPOWER(posX)
        except:
            logger.error('No file')
            posX += 1
        try:
            rep_to_excel.RSSI_RXANT_get()
            posX = write_RX_ANTRSSI(posX)
        except:
            logger.error('No file')
            posX += 1
        try:
            rep_to_excel.POWER_RXANT_get()
            write_RX_ANTPOWER(posX)
        except:
            logger.error('No file')
            posX += 1
        try:
            write_range_att(posX_txtp_avg, 66, posX_rxtp_avg, 2)
            write_range('DL', posX_txtp_avg, posX_APRSSI_avg, 20)
            write_range('UL', posX_rxtp_avg, posX_STARSSI_avg, 38)
        except:
            logger.error('No data')
        if ANGLE_NUM > 1:
            tx_tp = [float(tx.decode('ascii')) for tx in tx_tp]
            rx_tp = [float(rx.decode('ascii')) for rx in rx_tp]
            max_txtp = int(max(tx_tp)) + 100.0
            max_rxtp = int(max(rx_tp)) + 100.0
            write_radar(posX_txtp_avg - 1, 'B', max_txtp)
            write_radar(posX_rxtp_avg - 1, 'J', max_rxtp)
    set_properties()
    workbook.close()
    logger.info(filename)


if __name__ == "__main__":
    print('AP is ', DUT_NAME)
    Generate_Test_Report()
    
