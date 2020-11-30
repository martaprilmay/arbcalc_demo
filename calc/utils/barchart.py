import io
import numpy as np
import matplotlib.pyplot as plt

# data to plot
ai = ["ICC", "CSS"]
arb_fee = np.array([90, 95])
arbs_fee = np.array([50, 55])
admin_fee = [40, 40]

# creating bars

# width
bar_width = 0.3
# placing
# bar1 = np.arange(len(ai))
# bar2 = [i + bar_width for i in bar1]
# bar3 = [i + 2 * bar_width for i in bar1]

ind = [x for x, _ in enumerate(ai)]

plt.bar(ind, admin_fee, width=0.8, label='Administrative Fee', color='silver', bottom=arbs_fee)
plt.bar(ind, arbs_fee, width=0.8, label='Arbitrators Fee', color='gray',)

# plt.bar(ind, bronzes, width=0.8, label='bronzes', color='#CD853F')

# labels
# plt.xlabel('Arbitral Institutions')
plt.ylabel('Arbitration Fee in USD')
plt.xticks(ind, ai)
plt.legend()

chart = io.BytesIO()

plt.savefig('chart', dpi=400)
plt.show()


    # creating temp file
    # chart_path = os.path.join(tempfile.gettempdir(), 'chart.png')
    # plt.savefig(chart_path, dpi=100)
    # plt.close()

    # tmp = tempfile.NamedTemporaryFile('wb')
    # tmp.name = 'chart.png'
    # buf_chart.seek(0)
    # tmp.write(buf_chart.read())

    # # creating PDF with chart
    # pdf = FPDF(orientation='L', unit='mm', format='A4')
    # pdf.set_left_margin(0)
    # pdf.set_top_margin(0)
    # pdf.add_page()
    # pdf.set_xy(0, 0)
    # pdf.set_fill_color(240, 240, 240)
    # pdf.set_font('Helvetica', 'B', 12)
    # pdf.cell(297, 210, fill=True)
    #
    #
    #
    # WIDTH = 270
    # pdf.image('chart.png', 20, 5, WIDTH)
    #
    # pdf.output('results.pdf', 'f')
    #
    # with open('results.pdf', 'rb') as f:
    #     buf_pdf = io.BytesIO()
    #     buf_pdf.write(f.read())
    # # # print(2)
    # # # saving PDF to memory stream as a byte string
    # #
    # # buf_pdf = io.BytesIO()
    # # buf_pdf.write(pdf.output(dest='S').encode())
    # # print(3)
    # # creating response
