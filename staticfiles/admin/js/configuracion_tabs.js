// Script para agregar pestañas al admin de ConfiguracionSistema
(function($) {
    'use strict';
    
    console.log('✅ Script configuracion_tabs.js cargado');
    
    function initConfigTabs() {
        // Solo ejecutar en la página de ConfiguracionSistema
        if (window.location.href.indexOf('configuracionsistema') === -1) {
            return;
        }
        
        console.log('🚀 Inicializando tabs para ConfiguracionSistema');
        
        // Buscar todos los fieldsets
        var $fieldsets = $('fieldset.module, fieldset.collapse');
        console.log('📊 Fieldsets encontrados:', $fieldsets.length);
        
        if ($fieldsets.length === 0) {
            console.log('❌ No se encontraron fieldsets, reintentando...');
            setTimeout(initConfigTabs, 500);
            return;
        }
        
        // Agregar pestañas si no existen
        if ($('.config-admin-tabs').length === 0) {
            var tabsHtml = '<div class="config-admin-tabs" style="border-bottom: 2px solid #ddd; margin: 20px 0 0 0; padding: 0; background: #fff;">' +
                '<ul style="list-style: none; margin: 0; padding: 0; display: flex; gap: 5px; padding-left: 10px;">' +
                '<li style="margin: 0;"><a href="#" class="config-tab-link active" data-tab="empresa" style="display: block; padding: 12px 20px; background: #f5f5f5; border: 1px solid #ddd; border-bottom: none; text-decoration: none; color: #666; font-weight: 500; border-radius: 4px 4px 0 0; cursor: pointer;">🏢 Información de la Empresa</a></li>' +
                '<li style="margin: 0;"><a href="#" class="config-tab-link" data-tab="pagos" style="display: block; padding: 12px 20px; background: #f5f5f5; border: 1px solid #ddd; border-bottom: none; text-decoration: none; color: #666; font-weight: 500; border-radius: 4px 4px 0 0; cursor: pointer;">💳 Configuración de Pagos</a></li>' +
                '<li style="margin: 0;"><a href="#" class="config-tab-link" data-tab="colores" style="display: block; padding: 12px 20px; background: #f5f5f5; border: 1px solid #ddd; border-bottom: none; text-decoration: none; color: #666; font-weight: 500; border-radius: 4px 4px 0 0; cursor: pointer;">🎨 Colores del Sistema</a></li>' +
                '<li style="margin: 0;"><a href="#" class="config-tab-link" data-tab="preview" style="display: block; padding: 12px 20px; background: #f5f5f5; border: 1px solid #ddd; border-bottom: none; text-decoration: none; color: #666; font-weight: 500; border-radius: 4px 4px 0 0; cursor: pointer;">👁️ Vista Previa</a></li>' +
                '<li style="margin: 0;"><a href="#" class="config-tab-link" data-tab="info" style="display: block; padding: 12px 20px; background: #f5f5f5; border: 1px solid #ddd; border-bottom: none; text-decoration: none; color: #666; font-weight: 500; border-radius: 4px 4px 0 0; cursor: pointer;">ℹ️ Información</a></li>' +
                '</ul></div>';
            
            // Insertar antes del primer fieldset
            $fieldsets.first().before(tabsHtml);
            console.log('✅ Pestañas agregadas');
        }
        
        // Agregar clases a los fieldsets
        $fieldsets.each(function() {
            var $fieldset = $(this);
            var title = $fieldset.find('h2').text().trim();
            
            console.log('📋 Procesando fieldset:', title);
            
            // Remover clases anteriores
            $fieldset.removeClass('config-tab-empresa config-tab-pagos config-tab-colores config-tab-preview config-tab-info config-tab-active');
            
            if (title.indexOf('Información de la Empresa') !== -1) {
                $fieldset.addClass('config-tab-empresa');
                console.log('  ✅ Marcado como config-tab-empresa');
            } else if (title.indexOf('Configuración de Pagos') !== -1) {
                $fieldset.addClass('config-tab-pagos');
                console.log('  ✅ Marcado como config-tab-pagos');
            } else if (title.indexOf('Colores') !== -1) {
                $fieldset.addClass('config-tab-colores');
                console.log('  ✅ Marcado como config-tab-colores');
            } else if (title.indexOf('Vista previa') !== -1 || title.indexOf('Vista Previa') !== -1 || title.toLowerCase().indexOf('preview') !== -1) {
                $fieldset.addClass('config-tab-preview');
                console.log('  ✅ Marcado como config-tab-preview');
            } else if (title.indexOf('Información') !== -1 && title.indexOf('Empresa') === -1) {
                $fieldset.addClass('config-tab-info');
                console.log('  ✅ Marcado como config-tab-info');
            }
        });
        
        // Aplicar estilos CSS inline para ocultar/mostrar
        $fieldsets.css('display', 'none');
        var $firstTab = $('.config-tab-empresa');
        if ($firstTab.length > 0) {
            $firstTab.css('display', 'block').addClass('config-tab-active');
            console.log('✅ Mostrando config-tab-empresa');
        } else if ($fieldsets.length > 0) {
            $fieldsets.first().css('display', 'block').addClass('config-tab-active');
            console.log('✅ Mostrando primer fieldset');
        }
        
        // Manejar clics en las pestañas
        $('.config-tab-link').off('click.configtabs').on('click.configtabs', function(e) {
            e.preventDefault();
            var tab = $(this).data('tab');
            console.log('🔵 Click en tab:', tab);
            
            // Actualizar pestañas activas
            $('.config-tab-link').removeClass('active').css({
                'background': '#f5f5f5',
                'color': '#666',
                'border-bottom-color': '#ddd'
            });
            $(this).addClass('active').css({
                'background': 'white',
                'color': '#417690',
                'border-bottom-color': 'white',
                'position': 'relative',
                'top': '1px'
            });
            
            // Ocultar todos los fieldsets
            $fieldsets.css('display', 'none').removeClass('config-tab-active');
            
            // Mostrar el seleccionado
            var $target = $('.config-tab-' + tab);
            if ($target.length > 0) {
                $target.css('display', 'block').addClass('config-tab-active');
                console.log('✅ Mostrando config-tab-' + tab);
            } else {
                console.log('❌ No se encontró config-tab-' + tab);
            }
        });
        
        console.log('✅ Configuración de tabs completada');
    }
    
    // Ejecutar cuando jQuery esté listo
    if (typeof django !== 'undefined' && django.jQuery) {
        django.jQuery(document).ready(function() {
            setTimeout(initConfigTabs, 100);
            setTimeout(initConfigTabs, 500);
            setTimeout(initConfigTabs, 1000);
        });
    } else if (typeof jQuery !== 'undefined') {
        jQuery(document).ready(function() {
            setTimeout(initConfigTabs, 100);
            setTimeout(initConfigTabs, 500);
            setTimeout(initConfigTabs, 1000);
        });
    } else {
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(initConfigTabs, 500);
            setTimeout(initConfigTabs, 1000);
            setTimeout(initConfigTabs, 2000);
        });
    }
})(typeof django !== 'undefined' && django.jQuery ? django.jQuery : typeof jQuery !== 'undefined' ? jQuery : null);


