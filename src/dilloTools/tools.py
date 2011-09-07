"""Definition of all Dillo Tools"""


def addAllTools(d):
    """Build all categories and tools for the current version"""
    
    d.clearAllTools()
    d.addCat('Modeling', color=[73, 103, 55], colorDepth=255)
    d.addMelTool('Remove Crease', 'boRemovePolyCrease;', 'removePolyCrease.png')
    d.addMelTool('Mirror Geometry with Crease', 'boMirrorGeometryCrease;', 'mirrorGeometryCrease.png')
    d.addMelTool('Roadkill', 'RoadKill;', 'roadkill.png')
    d.addMelTool('Face Putty', 'facePutty;', 'facePutty.png')
    d.addMelTool('Symmetry Tool', 'source abSymMesh.mel; abSymMesh;', 'abSymmMesh.png')
    d.addMelTool('Blend Taper', 'source blendTaper.mel; blendTaper;', 'blendTaper.png')
    d.addMelTool('Multi Blend Slider', 'source boBlendShapes; bbsMultiBlendSlider;', 'multiBlendSlider.png')
    d.addMelTool('Add Inbetweens', 'source boBlendShapes; bbsAddInbetween;', 'addInBetween.png')
    d.addMelTool('Add Inbetweens - Auto', 'source boBlendShapes; bbsAddInbetweenAuto;', 'addInBetweenAuto.png')
    d.addMelTool('Blendshape Head Rebuilder', 'mdBlendCorrect;', 'blendCorrect.png')
    d.addMelTool('Blendshape Resurrector', 'source bRes.mel; bRes;', 'blendResurrect.png')
    
    d.addCat('Rigging', color=[75, 115, 145], colorDepth=255)
    d.addMelTool('Triggers', 'source boTriggers; boTriggers;', 'boTriggers.png')
    d.addMelTool('TSM Tools', 'source boTSMTools; boTSMTools;', 'TSMTools.png')
    d.addMelTool('boUtilities', 'source boUtilities; boUtilities;', 'boUtilities.png')
    d.addPyTool('Resetter', 'import boResetter\nreload(boResetter)\nboResetter.GUI()', 'resetter.png', annotation='A tool for resetting animation controls easily')
    d.addMelTool('Rigging Tools', 'dwRiggingTools;', 'dwRiggingTools.png')
    d.addMelTool('js Facial', 'jsFacial;', 'jsFacial.png')
    d.addMelTool('boSliders', 'source boSliders; boSliders;', 'boSliders.png')
    d.addMelTool('Preset Curve Controllers', 'rig101WireControllers;', 'wire.png')
    d.addMelTool('Parent to Surface', 'parentToSurface;', 'parentToSurface.png')
    d.addMelTool('Taffy', 'source taffy.mel; taffy;', 'taffy.png')
    d.addMelTool('Comet Rename', 'cometRename;', 'rename.png')
    
    d.addCat('Animation', color=[101, 31, 35], colorDepth=255)
    d.addMelTool('Grease Pencil', 'js_greasePencil_4;', 'greasePencil.png')
    d.addMelTool('Perfect Arc', 'perfectArc;', 'perfectArc.png')
    d.addMelTool('Pose Library', 'source poseLib_0452.mel; poseLib;', 'poseLibrary.png')
    d.addMelTool('Retimer', 'source retimingTool_090c.mel; retimingTool;', 'retimer.png')
    d.addMelTool('abx Picker', 'abxPicker;', 'abxPicker.png')
    d.addMelTool('boSmear', 'source boSmear; boSmear;', 'boSmear.png')
    d.addPyTool('ZV Parent Master', 'import ZvParentMaster\nZvParentMaster.ZvParentMaster()', 'ZVParentMaster.png')
    d.addMelTool('Onion Skin', 'source OnionSkin.mel; goOnion();', 'onionSkin.png')
    d.addPyTool('Pencil Tools GUI', 'import boPencilTools as pencil\npencil.GUI()', 'pencilGUI.png')
    d.addPyTool('Export to Pencil', 'import boPencilTools as pencil\npencil.export()', 'pencilExport.png')
    d.addPyTool('Run Pencil', 'import boPencilTools as pencil\npencil.runPencil()', 'pencilRun.png')
    
    d.addCat('Misc', color=[110, 112, 120], colorDepth=255)
    d.addMelTool('Camera Tools', 'cameraTools;', 'camTools.png')
    d.addMelTool('Hypergraph Window', 'HypergraphHierarchyWindow;', 'hypergraph.png')
    d.addMelTool('Hypershade Window', 'HypershadeWindow;', 'hypershade.png')
    d.addMelTool('Incremental Save', 'incrementalSave;', 'incSave.png')

