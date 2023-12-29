def mouseMoved(evt): 
    pos = evt[0] 
    if signalgraph.sceneBoundingRect().contains(pos): 
     mousePoint = vb.mapSceneToView(pos) 
     index = int(mousePoint.x()) 
     if index > 0 and index < len(x): 
      label.setText("<span style='font-size: 12pt'>x=%0.1f, <span style='color: red'>y1=%0.1f</span>" % (mousePoint.x(), y[index], data2[index])) 
     vLine.setPos(mousePoint.x()) 
     hLine.setPos(mousePoint.y()) 


signalgraph.scene().sigMouseMoved.connect(mouseMoved) 