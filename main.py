#!/usr/bin/env python

# http://docs.sqlalchemy.org/en/rel_1_0/orm/tutorial.html
# http://docs.sqlalchemy.org/en/rel_1_0/orm/relationships.html

from sys import argv
from datetime import date
from db import Session, Autoart, Ausstattung, Automodell
from db import Auto, Kunde, Fuehrerschein, Reservierung
from dataset import initialize
import wx
import wx.dataview

TEXT_BEZEICHNUNG = "- Bezeichnung -"
TEXT_HERSTELLER = "- Hersteller -"
TEXT_AUTOART = "- Autoart -"
TEXT_SITZPLAETZE = "- Sitzplaetze -"
TEXT_TREIBSTOFF = "- Treibstoff -"

def pydate2wxdate(d):
    assert isinstance(d, date)
    tt = d.timetuple()
    dmy = (tt[2], tt[1] - 1, tt[0])
    return wx.DateTimeFromDMY(*dmy)

def wxdate2pydate(d):
    assert isinstance(d, wx.DateTime)
    if d.IsValid():
        ymd = map(int, d.FormatISODate().split('-'))
        return date(*ymd)
    else:
        return None

class MainFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        MenuBar = wx.MenuBar()
        FileMenu = wx.Menu()
        MenuBar.Append(FileMenu, "&File")
        self.SetMenuBar(MenuBar)
        item = FileMenu.Append(wx.ID_EXIT, text = "&Exit")
        self.Bind(wx.EVT_MENU, self.OnQuit, item)
        self.Bind(wx.EVT_CLOSE, self.OnQuit)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.table = wx.dataview.DataViewListCtrl(self)
        self.table.AppendTextColumn("ID", width = 25)
        self.table.AppendTextColumn("Bezeichnung", width = 80)
        self.table.AppendTextColumn("Hersteller", width = 70)
        self.table.AppendTextColumn("Autoart", width = 70)
        self.table.AppendTextColumn("Sitzplaetze", width = 25)
        self.table.AppendTextColumn("KW", width = 30)
        self.table.AppendTextColumn("Treibstoff", width = 50)
        self.table.AppendTextColumn("Preis/Tag", width = 40)
        self.table.AppendTextColumn("Preis/KM", width = 40)
        self.table.AppendTextColumn("Achsen", width = 25)
        self.table.AppendTextColumn("Ladevolumen", width = 40)
        self.table.AppendTextColumn("Zuladung", width = 40)
        self.table.AppendTextColumn("Fuehrerschein", width = 25)
        self.table.AppendTextColumn("Autos", width = 25)
        self.table.AppendTextColumn("Ausstattungen", width = 150)
        self.table.SetMinSize((-1, 120))
        self.table.Bind(wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.CheckReservationValidity)
        sizer.Add(self.table, 1, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, 5)
        sizer.AddSpacer(2)

        searchPanel = wx.Panel(self)
        panelSizer = wx.BoxSizer(wx.HORIZONTAL)
        searchPanel.SetSizer(panelSizer)
        sizer.Add(searchPanel, 0, wx.EXPAND)

        self.comboBezeichnung = wx.ComboBox(searchPanel, style = wx.CB_READONLY)
        self.comboBezeichnung.SetMinSize((140, -1))
        self.comboBezeichnung.Bind(wx.EVT_COMBOBOX, self.OnComboBox)
        panelSizer.Add(self.comboBezeichnung, 0, wx.LEFT | wx.TOP, 5)

        self.comboHersteller = wx.ComboBox(searchPanel, style = wx.CB_READONLY)
        self.comboHersteller.SetMinSize((140, -1))
        self.comboHersteller.Bind(wx.EVT_COMBOBOX, self.OnComboBox)
        panelSizer.AddStretchSpacer(1)
        panelSizer.Add(self.comboHersteller, 0, wx.TOP, 5)

        self.comboAutoart = wx.ComboBox(searchPanel, style = wx.CB_READONLY)
        self.comboAutoart.SetMinSize((100, -1))
        self.comboAutoart.Bind(wx.EVT_COMBOBOX, self.OnComboBox)
        panelSizer.AddStretchSpacer(1)
        panelSizer.Add(self.comboAutoart, 0, wx.TOP, 5)

        self.comboSitzplaetze = wx.ComboBox(searchPanel, style = wx.CB_READONLY)
        self.comboSitzplaetze.SetMinSize((120, -1))
        self.comboSitzplaetze.Bind(wx.EVT_COMBOBOX, self.OnComboBox)
        panelSizer.AddStretchSpacer(1)
        panelSizer.Add(self.comboSitzplaetze, 0, wx.TOP, 5)

        self.comboTreibstoff = wx.ComboBox(searchPanel, style = wx.CB_READONLY)
        self.comboTreibstoff.SetMinSize((110, -1))
        self.comboTreibstoff.Bind(wx.EVT_COMBOBOX, self.OnComboBox)
        panelSizer.AddStretchSpacer(1)
        panelSizer.Add(self.comboTreibstoff, 0, wx.RIGHT | wx.TOP, 5)

        self.kunden = wx.dataview.DataViewListCtrl(self)
        self.kunden.AppendTextColumn("ID", width = 25)
        self.kunden.AppendTextColumn("Vorname", width = 50)
        self.kunden.AppendTextColumn("Nachname", width = 70)
        self.kunden.AppendTextColumn("PLZ", width = 45)
        self.kunden.AppendTextColumn("Ort", width = 80)
        self.kunden.AppendTextColumn("Strasse", width = 100)
        self.kunden.AppendTextColumn("EMail", width = 80)
        self.kunden.AppendTextColumn("TelNr", width = 80)
        self.kunden.AppendTextColumn("Fuehrerscheine", width = 30)
        self.kunden.SetMinSize((-1, 120))
        self.kunden.Bind(wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.CheckReservationValidity)
        sizer.Add(self.kunden, 1, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)

        datePanel = wx.Panel(self)
        dateSizer = wx.BoxSizer(wx.HORIZONTAL)
        datePanel.SetSizer(dateSizer)
        sizer.Add(datePanel, 0, wx.EXPAND)

        self.startDate = wx.DatePickerCtrl(datePanel)
        self.startDate.SetValue(pydate2wxdate(date.today()))
        self.startDate.Bind(wx.EVT_DATE_CHANGED, self.CheckReservationValidity)
        dateSizer.Add(self.startDate, 1, wx.LEFT | wx.RIGHT, 5)

        self.endDate = wx.DatePickerCtrl(datePanel)
        self.endDate.SetValue(pydate2wxdate(date.today()))
        self.endDate.Bind(wx.EVT_DATE_CHANGED, self.CheckReservationValidity)
        dateSizer.Add(self.endDate, 1, wx.LEFT | wx.RIGHT, 5)

        self.reservieren = wx.Button(datePanel, label = "Reservieren")
        self.reservieren.Enable(False)
        self.reservieren.Bind(wx.EVT_BUTTON, self.OnButton)
        dateSizer.Add(self.reservieren, 2, wx.EXPAND | wx.RIGHT | wx.BOTTOM | wx.TOP, 5)

        self.reservierungen = wx.dataview.DataViewListCtrl(self)
        self.reservierungen.AppendTextColumn("ID", width = 25)
        self.reservierungen.AppendTextColumn("Kunde", width = 150)
        self.reservierungen.AppendTextColumn("Automodell", width = 150)
        self.reservierungen.AppendTextColumn("Beginn", width = 100)
        self.reservierungen.AppendTextColumn("Ende", width = 100)
        self.reservierungen.Bind(wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, self.UnselectRow)
        sizer.Add(self.reservierungen, 1, wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)

        self.status = wx.StaticText(self, label = "Status: Bereit")
        sizer.Add(self.status, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 5)

        session = Session()
        dataset = session.query(Automodell).outerjoin(Auto).outerjoin(Ausstattung, Automodell.ausstattungen)
        self.UpdateComboBoxes(dataset)
        self.SetTable(dataset)
        self.SetKunden(session)
        self.SetReservierungen(session)
        session.commit()
        self.SetSizerAndFit(sizer)
        self.Centre()
        self.Show()

        if "test" in argv:
            wx.FutureCall(500, self.TestProcedure)

    def TestProcedure(self):
        self.table.SelectRow(0)
        self.kunden.SelectRow(0)
        self.OnButton(self)

    def UnselectRow(self, event):
        if self.reservierungen.GetSelectedRow() != wx.NOT_FOUND:
            self.reservierungen.UnselectRow(self.reservierungen.GetSelectedRow())

    def SetReservierungen(self, session):
        self.reservierungen.DeleteAllItems()
        data = session.query(Reservierung).outerjoin(Automodell).outerjoin(Kunde)
        for d in data:
            row = ["{}".format(d.id),
                   "{} {} ({})".format(d.kunde.vorname, d.kunde.nachname, d.kunde.id),
                   "{} {} ({})".format(d.modell.hersteller, d.modell.bezeichnung, d.modell.id),
                   "{}".format(d.beginn.date()), "{}".format(d.ende.date())]
            self.reservierungen.AppendItem(row)

    def SetKunden(self, session):
        self.kunden.DeleteAllItems()
        data = session.query(Kunde).outerjoin(Fuehrerschein)
        for d in data:
            row = ["{}".format(d.id), "{}".format(d.vorname),
                   "{}".format(d.nachname), "{}".format(d.plz),
                   "{}".format(d.ort), "{}".format(d.strasse),
                   "{}".format(d.email), "{}".format(d.telnr)]
            fs = ""
            for f in d.fuehrerscheine:
                fs = fs + f.klasse + "; "
            row.append(fs[:-2])
            self.kunden.AppendItem(row)

    def SetTable(self, data):
        self.table.DeleteAllItems()
        for d in data:
            row = ["{}".format(d.id), "{}".format(d.bezeichnung),
                   "{}".format(d.hersteller), "{}".format(d.autoart.art),
                   "{}".format(d.sitzplaetze), "{}".format(d.kw),
                   "{}".format(d.treibstoff), "{}".format(d.preistag),
                   "{}".format(d.preiskm), "{}".format(d.achsen),
                   "{}".format(d.ladevolumen), "{}".format(d.zuladung),
                   "{}".format(d.fuehrerschein), "{}".format(len(d.autos))]
            ausstt = ""
            for a in d.ausstattungen:
                ausstt += a.bezeichnung + "; "
            row.append(ausstt[:-2])
            self.table.AppendItem(row)

    def UpdateComboBoxes(self, data):
        bezeichnung = [TEXT_BEZEICHNUNG]
        hersteller = [TEXT_HERSTELLER]
        autoarten = [TEXT_AUTOART]
        sitzplaetze = [TEXT_SITZPLAETZE]
        treibstoff = [TEXT_TREIBSTOFF]

        for d in data:
            listPairs = [[d.bezeichnung, bezeichnung],
                         [d.hersteller, hersteller],
                         [d.autoart.art, autoarten],
                         ["{}".format(d.sitzplaetze), sitzplaetze],
                         [d.treibstoff, treibstoff]]
            for p in listPairs:
                if p[0] not in p[1]:
                    p[1].append(p[0])

        updatePairs = [[self.comboBezeichnung, bezeichnung, TEXT_BEZEICHNUNG],
                [self.comboHersteller, hersteller, TEXT_HERSTELLER],
                [self.comboAutoart, autoarten, TEXT_AUTOART],
                [self.comboSitzplaetze, sitzplaetze, TEXT_SITZPLAETZE],
                [self.comboTreibstoff, treibstoff, TEXT_TREIBSTOFF]]

        for p in updatePairs:
            found = False
            old = p[0].GetStringSelection()
            p[0].Set(p[1])
            for i in p[1]:
                if i == old:
                    p[0].SetStringSelection(i)
                    found = True
            if not found:
                p[0].SetStringSelection(p[2])

    def CheckReservationValidity(self, event):
        self.reservieren.Enable(False)
        session = Session()
        self.SetReservierungen(session)
        if self.table.GetSelectedRow() == wx.NOT_FOUND:
            self.status.SetLabel("Status: Kein Automodell gewaehlt!")
            session.commit()
            return
        if self.kunden.GetSelectedRow() == wx.NOT_FOUND:
            self.status.SetLabel("Status: Kein Kunde gewaehlt!")
            session.commit()
            return
        startDate = wxdate2pydate(self.startDate.GetValue())
        if startDate < date.today():
            self.status.SetLabel("Status: Startdatum ungueltig!")
            session.commit()
            return
        endDate = wxdate2pydate(self.endDate.GetValue())
        if endDate < date.today():
            self.status.SetLabel("Status: Enddatum ungueltig!")
            session.commit()
            return
        if startDate > endDate:
            self.status.SetLabel("Status: Enddatum vor Startdatum!")
            session.commit()
            return
        automodell_id = self.table.GetTextValue(self.table.GetSelectedRow(), 0)
        automodell = session.query(Automodell).filter_by(id = automodell_id)[0]
        kunde_id = self.kunden.GetTextValue(self.kunden.GetSelectedRow(), 0)
        kunde = session.query(Kunde).filter_by(id = kunde_id)[0]
        found = False
        for f in kunde.fuehrerscheine:
            if f.klasse == automodell.fuehrerschein:
                found = True
        if not found:
            self.status.SetLabel("Status: Fuehrerschein nicht passend!")
            session.commit()
            return
        if self.CheckForReservations(automodell_id, session) <= 0:
            self.status.SetLabel("Status: Kein Auto frei!")
            session.commit()
            return
        self.status.SetLabel("Status: Bereit zum reservieren...")
        self.reservieren.Enable(True)
        session.commit()

    def CheckForReservations(self, automodell_id, session):
        query = session.query(Auto).filter_by(modell_id = automodell_id)
        count = 0
        startDate = wxdate2pydate(self.startDate.GetValue())
        endDate = wxdate2pydate(self.endDate.GetValue())
        for a in query:
            reservierungen = session.query(Reservierung).filter_by(modell_id = automodell_id)
            for r in reservierungen:
                if (r.beginn.date() <= endDate) and (r.ende.date() >= startDate):
                    count += 1
        return query.count() - count

    def OnComboBox(self, event):
        session = Session()
        query = session.query(Automodell).outerjoin(Auto).outerjoin(Ausstattung, Automodell.ausstattungen)
        if self.comboBezeichnung.GetValue() != TEXT_BEZEICHNUNG:
            query = query.filter(Automodell.bezeichnung == self.comboBezeichnung.GetValue())
        if self.comboHersteller.GetValue() != TEXT_HERSTELLER:
            query = query.filter(Automodell.hersteller == self.comboHersteller.GetValue())
        if self.comboAutoart.GetValue() != TEXT_AUTOART:
            query = query.join(Autoart)
            query = query.filter(Autoart.art == self.comboAutoart.GetValue())
        if self.comboSitzplaetze.GetValue() != TEXT_SITZPLAETZE:
            query = query.filter(Automodell.sitzplaetze == int(self.comboSitzplaetze.GetValue()))
        if self.comboTreibstoff.GetValue() != TEXT_TREIBSTOFF:
            query = query.filter(Automodell.treibstoff == self.comboTreibstoff.GetValue())
        self.UpdateComboBoxes(query)
        self.SetTable(query)
        session.commit()

    def OnButton(self, event):
        session = Session()
        automodell_id = self.table.GetTextValue(self.table.GetSelectedRow(), 0)
        if self.CheckForReservations(automodell_id, session) > 0:
            kunde_id = self.kunden.GetTextValue(self.kunden.GetSelectedRow(), 0)
            r = Reservierung(beginn = wxdate2pydate(self.startDate.GetValue()),
                             ende = wxdate2pydate(self.endDate.GetValue()),
                             modell_id = automodell_id, kunde_id = kunde_id)
            session.add(r)
            session.commit()
            wx.MessageBox("Reservierung erfolgreich!", "Erfolg", wx.OK)
        else:
            session.commit()
            wx.MessageBox("Kein Auto verfuegbar!", "Fehler", wx.OK)
        self.table.UnselectRow(self.table.GetSelectedRow())
        self.kunden.UnselectRow(self.kunden.GetSelectedRow())
        self.startDate.SetValue(pydate2wxdate(date.today()))
        self.endDate.SetValue(pydate2wxdate(date.today()))
        self.CheckReservationValidity(self)

    def OnQuit(self, event):
        self.Destroy()

class MainApp(wx.App):
    def __init__(self, *args, **kwargs):
        wx.App.__init__(self, *args, **kwargs)
        self.Bind(wx.EVT_ACTIVATE_APP, self.OnActivate)

    def OnInit(self):
        self.frame = MainFrame(parent = None, title = "Autoverleih - DaPro")
        return True

    def BringWindowToFront(self):
        self.GetTopWindow().Raise()

    def OnActivate(self, event):
        if event.GetActive():
            self.BringWindowToFront()
        event.Skip()

    def MacReopenApp(self):
        self.BringWindowToFront()

initialize()
app = MainApp(False)
app.MainLoop()

