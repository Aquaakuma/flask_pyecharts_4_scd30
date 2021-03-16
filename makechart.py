from flask.json import jsonify
import pandas as pd

from pyecharts import options as opts
from pyecharts.charts import Line, Bar, Grid
from pyecharts.globals import ThemeType


def ReadCSV(CSV_FILE_PATH): # 读取csv文件，输出json格式
    dataframe = pd.read_csv(CSV_FILE_PATH, skiprows=0, na_values=['missing'])

    return dataframe


def chart_json(dataframe):
    time_CO2 = dataframe[['time', 'CO2']].values.tolist()
    time_temp = dataframe[['time', 'temp']].values.tolist()
    rh = dataframe['rh'].values.tolist()
    time = dataframe['time'].values.tolist()

    return jsonify({
        "time": time,
        "temp": time_temp,
        "rh": rh,
        "CO2": time_CO2
    })


def line_datazoom_CO2(dataframe) -> Line:
    Line_CO2=(
        Line()
        .add_xaxis(
            dataframe['time'].values.tolist(),
        )  # 添加x轴
        
        .add_yaxis(
            series_name="CO2浓度",
            y_axis=dataframe['CO2'].values.tolist(),
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            # xaxis_opts=opts.AxisOpts(type_="time"),
            title_opts=opts.TitleOpts(title='实时CO2浓度折线图'),
            datazoom_opts=opts.DataZoomOpts(
                is_show=True,
                pos_bottom=-2,
                xaxis_index=[0,1,2],
                
            ),
            tooltip_opts=opts.TooltipOpts(
                is_show=True,
                trigger="axis",
                axis_pointer_type='cross',
            ),
        )
    )

    return Line_CO2


def bar_datazoom_rh(dataframe) -> Bar:
    Bar_rh=(
        Bar()
        
        .add_xaxis(
            dataframe['time'].values.tolist(),
        )  # 添加x轴
        .add_yaxis(
            series_name="湿度",
            y_axis=dataframe['rh'].values.tolist(),
            label_opts=opts.LabelOpts(is_show=True),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title='实时湿度柱状图',pos_top="66%"),
            legend_opts=opts.LegendOpts(pos_top="66%"),
        )
    )

    return Bar_rh


def line_datazoom_temp(dataframe) -> Line:
    Line_temp=(
        Line() # 生成line类型图表
        .add_xaxis(
            dataframe['time'].values.tolist(),
        )  # 添加x轴
        
        .add_yaxis(
            series_name="温度",
            y_axis=dataframe['temp'].values.tolist(),
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            is_smooth=True,
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title='实时温度面积图',pos_top="33%"),
            legend_opts=opts.LegendOpts(pos_top="33%"),
        )
    )

    return Line_temp


def grid_chart(dataframe) -> Grid:
    grid = (
        Grid(
            init_opts=opts.InitOpts(
            width="1200px", height="800px",
            #设置动画
            animation_opts=opts.AnimationOpts(animation_delay=1000, animation_easing="elasticOut"),
            )
        )

        .add(
            line_datazoom_CO2(dataframe), # 图表实例，仅 `Chart` 类或者其子类
            
            # grid 组件离容器右侧的距离。
            # right 的值可以是像 20 这样的具体像素值，可以是像 '20%' 这样相对于容器高宽的百分比。
            grid_opts=opts.GridOpts(pos_top="4%", height="24%")
        )
        .add(
            line_datazoom_temp(dataframe), # 图表实例，仅 `Chart` 类或者其子类
            
            # grid 组件离容器右侧的距离。
            # right 的值可以是像 20 这样的具体像素值，可以是像 '20%' 这样相对于容器高宽的百分比。
            grid_opts=opts.GridOpts(pos_bottom="39%", height="24%")
        )
        .add(
            bar_datazoom_rh(dataframe), # 图表实例，仅 `Chart` 类或者其子类
            
            # grid 组件离容器右侧的距离。
            # right 的值可以是像 20 这样的具体像素值，可以是像 '20%' 这样相对于容器高宽的百分比。
            grid_opts=opts.GridOpts(pos_bottom="6%", height="24%")
        )
        .dump_options_with_quotes()
    )

    return grid
