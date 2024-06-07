import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np

# Dependencies
from nba_api.stats.endpoints import shotchartdetail, commonplayerinfo
from nba_api.stats.static import players, teams
import matplotlib.pyplot as plt
import numpy as np



class NBA_Stats:
    # def __init__(self):
    def get_player_info(self, player_name):
        player_id = players.find_players_by_full_name(player_name)[0]["id"]
        player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
        team_id = player_info.get_normalized_dict()['CommonPlayerInfo'][0]['TEAM_ID']
        return player_id, team_id, player_info.get_normalized_dict()

    def get_shot_chart(self, player_id, team_id, year, season_type="Regular Season", context_measure_simple="FGA"):
        shot_chart = shotchartdetail.ShotChartDetail(team_id=team_id, player_id=player_id, season_type_all_star="Regular Season",
                                                        season_nullable=year, context_measure_simple="FGA")
        league_average = shot_chart.league_averages.get_data_frame().rename(columns={'FGA': 'FGA_LA', 'FGM': 'FGM_LA', 'FG_PCT': 'FG_PCT_LA'})
        return shot_chart.shot_chart_detail.get_data_frame(), league_average

    def draw_plotly_court(self, fig, fig_width=600, margins=10):
        # From: https://community.plot.ly/t/arc-shape-with-path/7205/5
        def ellipse_arc(x_center=0.0, y_center=0.0, a=10.5, b=10.5, start_angle=0.0, end_angle=2 * np.pi, N=200, closed=False):
            t = np.linspace(start_angle, end_angle, N)
            x = x_center + a * np.cos(t)
            y = y_center + b * np.sin(t)
            path = f'M {x[0]}, {y[0]}'
            for k in range(1, len(t)):
                path += f'L{x[k]}, {y[k]}'
            if closed:
                path += ' Z'
            return path

        fig_height = fig_width * (470 + 2 * margins) / (500 + 2 * margins)
        fig.update_layout(width=fig_width, height=fig_height)

        # Set axes ranges
        fig.update_xaxes(range=[-250 - margins, 250 + margins])
        fig.update_yaxes(range=[-52.5 - margins, 417.5 + margins])

        threept_break_y = 89.47765084
        three_line_col = "#777777"
        main_line_col = "#777777"

        fig.update_layout(
            # Line Horizontal
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor="white",
            plot_bgcolor="white",
            yaxis=dict(
                scaleanchor="x",
                scaleratio=1,
                showgrid=False,
                zeroline=False,
                showline=False,
                ticks='',
                showticklabels=False,
                fixedrange=True,
            ),
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=False,
                ticks='',
                showticklabels=False,
                fixedrange=True,
            ),
            shapes=[
                dict(
                    type="rect", x0=-250, y0=-52.5, x1=250, y1=417.5,
                    line=dict(color=main_line_col, width=1),
                    # fillcolor='#333333',
                    layer='below'
                ),
                dict(
                    type="rect", x0=-80, y0=-52.5, x1=80, y1=137.5,
                    line=dict(color=main_line_col, width=1),
                    # fillcolor='#333333',
                    layer='below'
                ),
                dict(
                    type="rect", x0=-60, y0=-52.5, x1=60, y1=137.5,
                    line=dict(color=main_line_col, width=1),
                                fillcolor='#333333',
                                layer='below'
                            ),
                            dict(
                                type="circle", x0=-60, y0=77.5, x1=60, y1=197.5, xref="x", yref="y",
                                line=dict(color=main_line_col, width=1),
                                fillcolor='#2f2f2f',
                                layer='below'
                            ),
                            dict(
                                type="line", x0=-60, y0=137.5, x1=60, y1=137.5,
                                line=dict(color=main_line_col, width=1),
                                layer='below'
                            ),

                            dict(
                                type="rect", x0=-2, y0=-7.25, x1=2, y1=-12.5,
                                line=dict(color="#ec7607", width=1),
                                fillcolor='#ec7607',
                            ),
                            dict(
                                type="circle", x0=-7.5, y0=-7.5, x1=7.5, y1=7.5, xref="x", yref="y",
                                line=dict(color="#ec7607", width=1),
                            ),
                            dict(
                                type="line", x0=-30, y0=-12.5, x1=30, y1=-12.5,
                                line=dict(color="#ec7607", width=1),
                            ),

                            dict(type="path",
                                path=ellipse_arc(a=40, b=40, start_angle=0, end_angle=np.pi),
                                line=dict(color=main_line_col, width=1), layer='below'),
                            dict(type="path",
                                path=ellipse_arc(a=237.5, b=237.5, start_angle=0.386283101, end_angle=np.pi - 0.386283101),
                                line=dict(color=main_line_col, width=1), layer='below'),
                            dict(
                                type="line", x0=-220, y0=-52.5, x1=-220, y1=threept_break_y,
                                line=dict(color=three_line_col, width=1), layer='below'
                            ),
                            dict(
                                type="line", x0=-220, y0=-52.5, x1=-220, y1=threept_break_y,
                                line=dict(color=three_line_col, width=1), layer='below'
                            ),
                            dict(
                                type="line", x0=220, y0=-52.5, x1=220, y1=threept_break_y,
                                line=dict(color=three_line_col, width=1), layer='below'
                            ),

                            dict(
                                type="line", x0=-250, y0=227.5, x1=-220, y1=227.5,
                                line=dict(color=main_line_col, width=1), layer='below'
                            ),
                            dict(
                                type="line", x0=250, y0=227.5, x1=220, y1=227.5,
                                line=dict(color=main_line_col, width=1), layer='below'
                            ),
                            dict(
                                type="line", x0=-90, y0=17.5, x1=-80, y1=17.5,
                                line=dict(color=main_line_col, width=1), layer='below'
                            ),
                            dict(
                                type="line", x0=-90, y0=27.5, x1=-80, y1=27.5,
                                line=dict(color=main_line_col, width=1), layer='below'
                            ),
                            dict(
                                type="line", x0=-90, y0=57.5, x1=-80, y1=57.5,
                                line=dict(color=main_line_col, width=1), layer='below'
                            ),
                            dict(
                                type="line", x0=-90, y0=87.5, x1=-80, y1=87.5,
                                line=dict(color=main_line_col, width=1), layer='below'
                            ),
                            dict(
                                type="line", x0=90, y0=17.5, x1=80, y1=17.5,
                                line=dict(color=main_line_col, width=1), layer='below'
                            ),
                            dict(
                                type="line", x0=90, y0=27.5, x1=80, y1=27.5,
                                line=dict(color=main_line_col, width=1), layer='below'
                            ),
                            dict(
                                type="line", x0=90, y0=57.5, x1=80, y1=57.5,
                                line=dict(color=main_line_col, width=1), layer='below'
                            ),
                            dict(
                                type="line", x0=90, y0=87.5, x1=80, y1=87.5,
                                line=dict(color=main_line_col, width=1), layer='below'
                            ),

                            dict(type="path",
                                path=ellipse_arc(y_center=417.5, a=60, b=60, start_angle=-0, end_angle=-np.pi),
                                line=dict(color=main_line_col, width=1), layer='below'),

            ]
        )
        return True

    # this is all assumming we are using the nba_api shot chart detail data
    def hex_shot_chart(self, player_name, season):
        # set gridsize for hexbin calculation
        gridsize = 30
        hex_color = '51, 255, 173,'
        fig_width = 600
        hex_size = 16
        source = 'nba.com/stats'
        left_annotation = 'Cole Wood'

        pio.templates["nba_stats"] = go.layout.Template(
            # LAYOUT
            layout = {
                # Fonts
                # Note - 'family' must be a single string, NOT a list or dict!
                'title':
                    {'font': {'family': 'Helvetica Nueue, Helvetica Nueue Light, Sans-serif',
                            'size':24,
                            'color': '#dcdcdc'}
                    },
                'font': {'family': 'Helvetica Neue, Helvetica Nueue Light, Sans-serif',
                            'size':12,
                            'color': '#dcdcdc'},
                },
            )
        
        # get playerinfo
        player_id, team_id, player_info = self.get_player_info(player_name)
        # return shotchart data (var inspired by BI)
        bi, league_average = self.get_shot_chart(player_id, team_id, season)

        # cluster by shots attempted
        shots_hex = plt.hexbin(
            bi['LOC_X'], bi['LOC_Y'],
            extent=(-250, 250, 422.5, -47.5), cmap='Blues', gridsize=gridsize)
        plt.close()  # this closes the plot window

        # cluster by shots made
        makes_df = bi[bi['SHOT_MADE_FLAG'] == 1]
        makes_hex = plt.hexbin(
            makes_df['LOC_X'], makes_df['LOC_Y'],
            extent=(-250, 250, 422.5, -47.5), cmap=plt.cm.Reds, gridsize=gridsize)
        plt.close()

        # calculate shot accuracy
        pcts_by_hex = makes_hex.get_array() / shots_hex.get_array()
        pcts_by_hex[np.isnan(pcts_by_hex)] = 0
        # calculate shot count
        shot_count_hex = shots_hex.get_array()
        shot_count_hex[np.isnan(shot_count_hex)] = 0

        # filter out low sample sizes
        filter_threshold = 1
        for i in range(len(pcts_by_hex)):
            if shot_count_hex[i] < filter_threshold:
                pcts_by_hex[i] = 0
                shot_count_hex[i] = 0
        xlocs = [i[0] for i in shots_hex.get_offsets()]
        ylocs = [i[1] for i in shots_hex.get_offsets()]
        accs_by_hex = pcts_by_hex

        # draw plotly chart
        fig = go.Figure()
        self.draw_plotly_court(fig, fig_width=fig_width)
        fig.add_trace(go.Scatter(
            x=xlocs, y=ylocs, mode='markers', name='markers',
            marker=dict(
                size=hex_size, 
                sizemode='area', 
                color=shot_count_hex,
                colorscale=[
                    [0, f'rgba({hex_color} 0.0)'],
                    [0.05, f'rgba({hex_color} 0.35)'],
                    [0.1, f'rgba({hex_color} 0.4)'],
                    [0.2, f'rgba({hex_color} 0.5)'],
                    [0.4, f'rgba({hex_color} 0.85)'],
                    [0.6, f'rgba({hex_color} 0.9)'],
                    [0.8, f'rgba({hex_color} 0.95)'],
                    [1, f'rgba({hex_color} 1.0)'],
                ],
                #line=dict(width=1, color='#333333'), 
                symbol='hexagon',
            ),
            text=[f'FGA: {sc}, FG_PCT: {ac}' for sc, ac in zip(shot_count_hex, accs_by_hex)],  # Add this line
        ))
        fig.update_layout(
            template='nba_stats',
            width = 500,
            margin=dict(l=5, r=5, t=80, b=20),
            title={
                'text': f"{player_name} - {player_info['CommonPlayerInfo'][0]['TEAM_ABBREVIATION']}<br><sub>{season} Shot Chart</sub>",
                'y':0.93,  # Adjust this value to move the title up or down
                'x':0.03,
                'xanchor': 'left',
                'yanchor': 'top'},
            paper_bgcolor=' #2f2f2f ',  # Set the color of the paper
            plot_bgcolor=' #2f2f2f ',  # Set the color of the plotting area
            
            annotations=[
                dict(
                    x=0.99,
                    y=-0.03,
                    showarrow=False,
                    text=f"source: {source}",
                    xref="paper",
                    yref="paper",
                ),
                dict(
                    x=0.01,
                    y=-0.03,
                    showarrow=False,
                    text=f"{left_annotation}",
                    xref="paper",
                    yref="paper",
                )
            ]
        )
        fig.update_xaxes(automargin='left+right')
        fig.show(config=dict(displayModeBar=True))