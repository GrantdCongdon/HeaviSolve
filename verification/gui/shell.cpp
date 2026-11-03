// SPDX-FileCopyrightText: 2026 HeaviSolve contributors
// SPDX-License-Identifier: AGPL-3.0-or-later
#include <QApplication>
#include <QDockWidget>
#include <QElapsedTimer>
#include <QGraphicsView>
#include <QGraphicsScene>
#include <QMainWindow>
#include <QPainter>
#include <QScreen>
#include <QStatusBar>
#include <QSurfaceFormat>
#include <QTextEdit>
#include <QTimer>
#include <QVTKOpenGLNativeWidget.h>
#include <vtkActor.h>
#include <vtkCutter.h>
#include <vtkGenericOpenGLRenderWindow.h>
#include <vtkImageData.h>
#include <vtkNew.h>
#include <vtkPlane.h>
#include <vtkPointData.h>
#include <vtkPolyData.h>
#include <vtkPolyDataMapper.h>
#include <vtkRenderer.h>
#include <vtkVersion.h>
#include <algorithm>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <vector>
class View final : public QGraphicsView {
public:
  using QGraphicsView::QGraphicsView;
  std::vector<double> paint_ms;
  bool recording=false;
protected:
  void paintEvent(QPaintEvent* event) override {
    QElapsedTimer timer;timer.start();QGraphicsView::paintEvent(event);
    if(recording) paint_ms.push_back(timer.nsecsElapsed()/1e6);
  }
};
int main(int argc,char** argv) {
  QSurfaceFormat::setDefaultFormat(QVTKOpenGLNativeWidget::defaultFormat());
  QApplication app(argc,argv);
  const bool million=argc>1 && std::string(argv[1])=="million";
  const std::string output=argc>2?argv[2]:"gui-spike.png";
  QMainWindow window;window.setWindowTitle("HeaviSolve — M0 feasibility");window.resize(1400,900);
  window.setStyleSheet("QMainWindow,QDockWidget,QTextEdit{background:#1e1e1e;color:#dddddd;} QStatusBar{background:#007acc;color:white;}");
  QGraphicsScene scene;
  const int side=million?1000:100;
  for(int y=0;y<side;++y) for(int x=0;x<side;++x) {
    QPolygonF polygon;polygon<<QPointF(x*10,y*10)<<QPointF(x*10+7,y*10)<<QPointF(x*10+7,y*10+6)<<QPointF(x*10,y*10+6);
    scene.addPolygon(polygon,QPen(Qt::NoPen),QBrush(QColor(60+(x%4)*30,140,190)));
  }
  scene.setSceneRect(0,0,side*10,side*10);
  View view(&scene);view.setBackgroundBrush(QColor(30,30,30));view.setViewportUpdateMode(QGraphicsView::FullViewportUpdate);
  window.setCentralWidget(&view);
  auto* explorer=new QDockWidget("Explorer / Process",&window);
  explorer->setWidget(new QTextEdit("HeaviSolve M0\nprocess: synthetic\ngeometry: deterministic grid\nsolver: none\n\nThis is a feasibility scene."));
  window.addDockWidget(Qt::LeftDockWidgetArea,explorer);
  auto* field=new QDockWidget("Results — manufactured field cut plane",&window);
  auto* widget=new QVTKOpenGLNativeWidget(field);field->setWidget(widget);
  window.addDockWidget(Qt::RightDockWidgetArea,field);
  widget->setMinimumSize(320,360);explorer->setMinimumWidth(220);field->setMinimumWidth(360);
  window.resizeDocks({explorer,field},{240,360},Qt::Horizontal);
  vtkNew<vtkGenericOpenGLRenderWindow> renderWindow;widget->setRenderWindow(renderWindow);
  vtkNew<vtkRenderer> renderer;renderWindow->AddRenderer(renderer);renderer->SetBackground(.12,.12,.12);
  vtkNew<vtkImageData> image;image->SetDimensions(31,31,31);image->SetOrigin(-1,-1,-1);image->SetSpacing(2./30,2./30,2./30);image->AllocateScalars(VTK_DOUBLE,1);
  for(int z=0;z<31;++z) for(int y=0;y<31;++y) for(int x=0;x<31;++x) {
    const double px=-1+x*2./30,py=-1+y*2./30,pz=-1+z*2./30;
    *static_cast<double*>(image->GetScalarPointer(x,y,z))=std::sin(3*px)*std::cos(3*py)+pz;
  }
  vtkNew<vtkPlane> plane;plane->SetOrigin(0,0,0);plane->SetNormal(.2,.1,1);
  vtkNew<vtkCutter> cutter;cutter->SetInputData(image);cutter->SetCutFunction(plane);cutter->Update();
  vtkNew<vtkPolyDataMapper> mapper;mapper->SetInputConnection(cutter->GetOutputPort());mapper->SetScalarRange(-1,1);
  vtkNew<vtkActor> actor;actor->SetMapper(mapper);renderer->AddActor(actor);renderer->ResetCamera();
  window.statusBar()->showMessage("M0 spike | no production solver | shared API architecture pending Phase R");
  window.show();
  int frames=0;QElapsedTimer elapsed;std::vector<double> intervals;double last=0;
  QTimer tick;tick.setInterval(0);
  QObject::connect(&tick,&QTimer::timeout,[&]{
    if(frames==60) { elapsed.start();view.recording=true;last=0; }
    const double phase=frames*.035;
    QTransform transform;const double scale=million?.8:1.;transform.scale(scale*(1+.1*std::sin(phase)),scale*(1+.1*std::sin(phase)));
    view.setTransform(transform);view.centerOn(side*5+100*std::sin(phase),side*5+100*std::cos(phase));
    view.viewport()->repaint();
    if(frames>=60) { const double now=elapsed.nsecsElapsed()/1e6;intervals.push_back(now-last);last=now; }
    ++frames;
    if(frames==300) {
      tick.stop();const double seconds=elapsed.nsecsElapsed()/1e9;
      auto sorted=view.paint_ms;std::sort(sorted.begin(),sorted.end());
      std::cout<<std::setprecision(17)<<"qt="<<QT_VERSION_STR<<" vtk="<<vtkVersion::GetVTKVersion()<<" platform="<<QGuiApplication::platformName().toStdString()<<" polygons="<<side*side<<" viewport_width="<<view.viewport()->width()<<" viewport_height="<<view.viewport()->height()<<" dpr="<<view.devicePixelRatioF()<<"\n"
        <<"frames="<<intervals.size()<<" seconds="<<seconds<<" viewport_repaint_fps="<<intervals.size()/seconds<<" paint_p95_ms="<<sorted[static_cast<std::size_t>(sorted.size()*.95)]<<" cutplane_cells="<<cutter->GetOutput()->GetNumberOfCells()<<"\n";
      const bool saved=window.grab().save(QString::fromStdString(output));
      std::cout<<"screenshot_saved="<<saved<<" compositor_present_rate=NOT_MEASURED\n";
      app.exit(saved && cutter->GetOutput()->GetNumberOfCells()>0 && intervals.size()/seconds>=60?0:1);
    }
  });
  QTimer::singleShot(1000,[&]{renderWindow->Render();tick.start();});
  return app.exec();
}
