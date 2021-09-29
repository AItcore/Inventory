import zpl
from zebra import Zebra


def printLabel(year, month, start, end):
    year = str(year)[2:]
    if month < 10:
        month = "0" + str(month)
    else:
        month = str(month)
    z = Zebra()
    queues = z.getqueues()
    for q in queues:
        if 'ZDesigner' in q:
            z.setqueue(q)
            break
    for i in range(start, end+1):
        label = zpl.Label(15, 30)
        label.origin(7, 2)
        label.write_barcode(height=120, barcode_type='C')
        if i < 10:
            label.write_text(f"SY{year}{month}00{i}")
        elif i < 100:
            label.write_text(f"SY{year}{month}0{i}")
        else:
            label.write_text(f"SY{year}{month}{i}")
        label.endorigin()
        z.output(label.dumpZPL())
